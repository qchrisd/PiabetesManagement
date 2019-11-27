# Piabetes Monitor ReadMe
This Project attempts to create a device to allow remote monitoring of a set of insulin syringes.

# Monitoring the syringe slots
The slots are monitored with the `slotMonitor.py` script. It watches the switches and performs an action based on the pin that was activated.

# Power Monitoring
The power of the device is handles with two separate scripts.

The first is `powerBoostMonitor.py` that will watch the PowerBoost 1000C charger connected to the device. When the PowerBoost is unplugged, an email is sent to the recipient. When the battery gets low, the device will call `shutdown.py` and shudown the pi gracefully.
