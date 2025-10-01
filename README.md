# The best RGB controller for retro handheld devices (WIP)

Currently planning to support:
 * all Anbernic H700 devices with RGB
 * A133P devices: TrimUI Smart Pro and Brick

### Available Options:
 * Modes (list)
 * Brightness
 * Adaptive Brightness
 * Palette (list)
   * Custom palette colors (either 2 rgb sliders, or 2 color lists)
 * Palette Swap
 * Split Palette (on devices that have secondary zones, like a second stick)
 * RA integration - not handled by the RGB Daemon
 * Battery Notifications (on, off, constant)

### API Endpoints

Default URL is `http://localhost:1235/` and the following endpoints are available:

#### `reload-config/` payload:`option_key`

Reloads the entire config and applies the changes, if `option_key` is specified, only that one option is reloaded.

#### `run-animation/` payload:`animation_list`

Runs animations specified in the payload, can be one or more, separated by `;`:
 * Preset: Preset calls contain premade animation lists
  * `battery_charging`
  * `battery_low`
  * `battery_full`
  * `cheevo`
 * Manual animation list:
  * `up green` - runs `up` with RGB(0,255,0) color
  * `blink #ff00ff 3` - runs `blink` 3 times in magenta
A full payload might look like: `blink green; battery_low; blink #ff00ff 3`

#### `update-battery-state/` payload:`percentage state`

Updates the battery state the daemon is aware of in an event driven way, percentage is a number 0-100, state is `Charging`|`Full`|`Discharging`

#### `update-screen-state/` payload:`percentage`

Updates the screen brightness state for adaptive brightness, takes a number 0-100

#### `get-animations/`

Returns the list of available animations in a json with all metadata

#### `get-modes/`

Returns the list of supported modes and metadata in a json

#### `get-palettes/`

Returns the list of available palettes in a json list

#### `get-options/`

Returns the list of available option keys and supported values where applicable based on the capabilities of the device.