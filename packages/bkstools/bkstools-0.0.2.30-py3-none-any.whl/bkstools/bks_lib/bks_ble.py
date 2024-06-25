'''
Created on 11.10.2023

@author: R001483
'''

import asyncio
from itertools import count, takewhile
from typing import Iterator
import time
from threading import Thread, current_thread

from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic

from bkstools.bks_lib.debug import Print, Error, Debug, Var, ApplicationError

use_dev = True
if (use_dev):
    spp_service_uuid             = "4880c12c-fdcb-4077-8920-a450d7f9b908"  # for development to not disturb others
    spp_data_characteristic_uuid = "fec26ec4-6d71-4442-9f81-55bc21d658d7"  # for development to not disturb others
else:
    spp_service_uuid             = "4880c12c-fdcb-4077-8920-a450d7f9b907"
    spp_data_characteristic_uuid = "fec26ec4-6d71-4442-9f81-55bc21d658d6"

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

def bytes_to_hex( bs ):
    """Return the bytes in bs as hex-values separated by space
    """
    r=""
    sep = ""
    for b in bs:
        r += sep + f"{b:02x}"
        sep = " "
    return r

g_device = None
ble_tx_queue = asyncio.Queue()
ble_rx_data = bytearray()
g_written = False
t_start = None
async def async_main( address ):
    global t_start
    global g_device, ble_tx_queue
    global g_written

    timeout_s = 5.0
    device = await BleakScanner.find_device_by_address( address, timeout_s )


    if ( not device ):
        raise( IOError( "BLE: Device not found" ) )

    Debug( f"BLE: Device found with addr {device.address}" )

    async with BleakClient( device,
                          ) as client:
        Debug("BLE: connected")

        try:
            await client.start_notify( spp_data_characteristic_uuid, spp_callback )

            loop = asyncio.get_running_loop()
            nus = client.services.get_service( spp_service_uuid )
            rx_char = nus.get_characteristic( spp_data_characteristic_uuid )

            Debug( f"BLE: rx_char.max_write_without_response_size={rx_char.max_write_without_response_size}" )
            g_device = device

            # from https://github.com/hbldh/bleak/blob/develop/examples/uart_service.py
            while True:

                # This waits until new data is availalablein ble_tx_queue
                data = await ble_tx_queue.get()

                if ( data is None ):
                    # None was put in queue to terminate the thread
                    Debug( f"BLE: terminating BLE thread" )
                    break
                Debug( f"BLE: data from queue{data} ")

                t_start = time.time()

                for s in sliced(data, rx_char.max_write_without_response_size):
                    Debug( f"BLE: Sending {s!r} = {bytes_to_hex(s)} ")
                    await client.write_gatt_char(rx_char, s, response=False)
                    g_written = True

                ble_tx_queue.task_done()

            #print("sent:", data)
            #response = await client.read_gatt_char( spp_data_characteristic_uuid )
            #Debug( f"response = {response!r} ({len(response)}" )
            #await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            # terminate silently
            pass
        finally:
            Debug("BLE: disconnecting...")
            await client.stop_notify( spp_data_characteristic_uuid )

    Debug("BLE: disconnected")
    g_device = None


def spp_callback( sender: BleakGATTCharacteristic, data: bytearray ):
    global t_start, ble_rx_data
    t_stop = time.time()
    Debug( f"BLE: spp_callback: {sender}: {data} {len(data)}")
    Debug( f'BLE: received "{data!r}" = {bytes_to_hex(data)} after {t_stop - t_start:.3f}s' )
    ble_rx_data += data

def run_asyncio( address ):
    try:
        asyncio.run( async_main( address ) )
    except KeyboardInterrupt:
        # terminate silently
        pass


class cBLESerial( object ):

    def __init__(self, address ):
        Debug( f"cBLESerial object created for address {address}" )
        self.address = address
        # port.address is something like DC:8E:95:58:2F:D9 which is not valid as a filename
        self.port = address.replace( ":", "_" )
        self._timeout = 0.3

        self.ble_thread = Thread( target=run_asyncio, args=[address] )
        self.ble_thread.start()

        global g_device
        while g_device is None:
            time.sleep(0.1)

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        Debug( f"cBLESerial timeout:={value}" )
        self._timeout = value

    def open(self):
        Debug( f"cBLESerial.open()" )
        pass

    def close(self):
        Debug( f"cBLESerial.close()" )
        ble_tx_queue.put_nowait( None ) # tell ble thread to terminate
        ble_tx_queue._loop._write_to_self()  # see https://stackoverflow.com/a/43275001
        self.ble_thread.join()
        Debug( f"cBLESerial.close(): joined" )
        pass

    def reset_input_buffer(self):
        Debug( f"cBLESerial.reset_input_buffer()" )
        pass

    def reset_output_buffer(self):
        Debug( f"cBLESerial.reset_output_buffer()" )
        pass

    def read(self, size):
        global ble_rx_data
        Debug( f"cBLESerial.read({size})" )
        t_end = time.time() + self._timeout
        while ( len( ble_rx_data ) < size and time.time() <= t_end ):
            pass

        data = bytes( ble_rx_data )
        ble_rx_data = bytearray()
        return data

    def write(self, data):
        global g_written
        Debug( f"cBLESerial.write({data!r})" )
        ble_tx_queue.put_nowait( data )
        ble_tx_queue._loop._write_to_self()  # see https://stackoverflow.com/a/43275001
        while ( not g_written ):
            pass
        g_written = False
        #asyncio.run( ble_tx_queue.put( data ) )

    @property
    def is_open(self):
        global g_device
        is_open = not g_device is None
        Debug( f"cBLESerial.is_open {is_open}" )
        return is_open

    def flush(self):
        Debug( f"cBLESerial.flush()" )
