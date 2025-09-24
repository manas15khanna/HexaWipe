# HexaWipe

HexaWipe is a web-based, Material You themed application designed as a user-friendly interface for securely wiping drives and Android devices. It includes clean, modern UI pages simulating various secure erase operations with interactive elements.

## Features

- **Home Page**: Select between Hard Drive, Solid State Drive, or Android device wiping.
- **Hard Drive & SSD Pages**: Choose drives, toggle recursive wipe option, and initiate wipe with a material-themed interface.
- **Android Page**: Three vertically stacked buttons to guide users through formatting, connect to ADB and wipe, or wipe again.
- **Wipe Progress Page**: Full-screen terminal-style simulation showing fake wipe commands and a progress bar over ~8 seconds.
- **Completion Redirect**: Automatically opens a certificate PDF in a new tab after wiping and redirects the main page to the homepage.
- Fully responsive Material You inspired UI with consistent design aesthetics.

## How It Works

- Users navigate through the linked pages selecting devices and wipe options.
- When "WIPE" is triggered, the user is taken to a wipe progress page that simulates the wiping process visually.
- Upon completion, a certificate PDF is displayed for verification or record keeping, while the app returns to the home page.

## Technologies

- HTML5, CSS3 (Material You inspired styles)
- JavaScript for interactivity and simulation
- Designed to be lightweight and easily extendable

## Getting Started

1. Download or clone this repository.
2. Place your device icon images (`hard_disk.png`, `solid_drive.png`, `mobile.png`) inside an `images/` folder.
3. Place `certificate.pdf` in the project root or update the path in the wipe progress page script.
4. Open `index.html` in any modern browser to start using HexaWipe.

## Customization

- Modify the wipe simulation script inside `wipe-progress.html` to link to actual wipe commands if integrated with backend.
- Add real device detection and wipe commands using server-side scripts or Electron integrations.
- Enhance the Android guide page with real ADB connectivity if desired.

## License

HexaWipe is provided as-is for educational and demonstration purposes.

---

Feel free to contribute or customize HexaWipe for your secure erasure needs!

