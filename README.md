<!-- TABLE OF CONTENTS -->

  ## Table of Contents
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>


<!-- GETTING STARTED -->
## Getting Started

This project is made up of few smaller 'projects'

* ESP32
* RaspberryPi
* Mobile Application


### Prerequisites

For this project you need to have ESP32 and a relay to control your intercom system, RaspberryPi with SenseHat and camera module, and Mobile phone (for Iphone you would need to build it yourself) running Android and have an Firebase account with Realtime Database, Storage.

In case you want everything to work outside your local network you will need to do Port forwarding or have a cloud hosting provider. (In my case)

* Required
  ```sh
  python3
  pip
  mosquito broker
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Ygnas/IoT-Application
   ```
2. Open the Firebase console and create a new project [https://console.firebase.google.com/](https://console.firebase.google.com/)
3. After your project is ready, you can create a Realtime Database.
4. In the Service Accounts tab Generate new private key
5. In RaspberryPi folder copy generated private key content to serviceAccountKey.json and fill up .env file
6. Install required packages to your *Raspberry Pi* and/or your cloud host (if using it)
   ```sh
   cd RaspberryPi
   pip install -r requirements.txt
   ```
7. Now you are ready to launch everything
   * On your *Raspberry Pi*
   ```sh
   python client.py
   ```
   * On your *cloud host*
   ```sh
   python server.py
   ```
   * If not using *cloud host* you can launch both on *Raspberry Pi* using tmux/screen
8. Flash your esp32 from ESP32 folder. (don't forget to fill up your details in AppSecrets.h)
9. Connect it to your intercom system (you will have to figure that your self as every system is different)
10. Install gate_app.apk to your android phone (or build it for Iphone) [https://firebase.google.com/docs/flutter/setup?platform=android/](https://firebase.google.com/docs/flutter/setup?platform=android/)
11. Open the gate from your phone 🤯😎🥳


<!-- USAGE EXAMPLES -->
## Usage

Open phone application, and press it to open.
<img src="https://raw.githubusercontent.com/Ygnas/IoT-Application/main/Screenshots/open.jpg" height="320">
<img src="https://raw.githubusercontent.com/Ygnas/IoT-Application/main/Screenshots/opening.jpg" height="320">

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue.
Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request