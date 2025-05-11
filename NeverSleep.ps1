function Set-NeverSleep
{
    # Set the system to never sleep on AC power
    powercfg -change -standby-timeout-ac 0

    # Set the system to never sleep on battery power
    powercfg -change -standby-timeout-dc 0

    # Set the display to never turn off on AC power
    powercfg -change -monitor-timeout-ac 0

    # Set the display to never turn off on battery power
    powercfg -change -monitor-timeout-dc 0
}
Set-NeverSleep