# RaspberryPi Backlight Integration

Home Assistant custom integration for controlling the brightness and screen power of the official 7" RaspberryPi
Touchscreen. Built to communicate with the [RaspberryPi Backlight Server](https://github.com/gannonprudhomme/RaspberryPi-Backlight-Server).

## Installation (via HACS)

0. The project is added as a custom repository from [HACS](), so make sure you have that installed first.

1. Add it as a custom repository in HACS:

    a. Go to HACS panel -> Integrations

    b. In the dropdown on the top right, click `Custom repositories`

    c. In the `Add custom repository URL` field, enter `https://github.com/gannonprudhomme/ha-rpi-backlight`
    and for `category` enter `Integration`.

    d. The repository should appear as a `New repository` on the `Integration` screen. If it doesn't,
    go to `+ Explore & Add Repositories` then search for it. You'll then need to restart HA.

    e. Then click `Install` to install it into `config/custom_components`

2. Add it to Home Assistant as you would any other integration, and enter the desktop's URL
during the config flow.

3. You can can optionally change the scanning interval in the
below Configuration step.

## Configuration

You can add the integration through Home Assistant's UI.

Additional, you can add the following to your `configuration.yaml`:

```yaml
rpi_backlight:
  scanning_interval: 5 # in seconds, defaults to 30
```

## Development

Due to Docker not allowing host networking on Windows, you must install Home Assistant manually
(`pip install wheel`, `pip install homeassistant`, `hass -c .`).
