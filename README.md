# remarkable_keyboard

Use your reMarkable as a wireless mouse and keyboard.

[Demo Video](https://peertube.live/videos/watch/f5f749f1-3ce0-4e0e-9946-b7a23dbef1ac)

<img src="photo.jpg" width=500>

# Usage

Copy [this pdf](resources/keyboard.pdf) to your device.

``` bash
pip install remarkable-keyboard
rekeyboard
```

By default, `10.11.99.1` is used as the address.

# Examples

``` bash
# specify address, password (listed under Settings > About)
rekeyboard --address 192.168.1.100 --password PASSWORD

# pubkey login
ssh-keygen -f ~/.ssh/remarkable -N ''
ssh-copy-id -i ~/.ssh/remarkable.pub root@10.11.99.1
rekeyboard --key ~/.ssh/remarkable
```
