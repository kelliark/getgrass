# GetGrass Farmer V2

Enhanced multi-account farming bot for GetGrass.io with proxy support and automatic proxy management.

> ⚠️ **Desktop mode is still in Development. Please use Extension mode!**

## Features
* Multi-Account Support
* Automatic Proxy Management & Rotation
* Smart Error Handling & Recovery
* Beautiful Console Output
* Wide Browser Support (Edge, Chrome, Firefox, Safari)
* Both Desktop & Mobile User Agents
* Failed Proxy Detection & Auto-Replacement

## Requirements
1. GetGrass.io Account UserID ([Register Here](https://app.getgrass.io))
2. Proxies (ISP Proxies Recommended)
3. VPS or RDP (OPTIONAL)
4. Python 3.10 or Later
5. Required packages:

## Proxy Setup
### Recommended Proxy Providers
- Premium ISP Proxies (Recommended):
  * [Proxiesfo](https://app.proxies.fo/ref/208a608a-0dbf-13c3-7651-7f5303fc5cb2)

## Getting Started

### 1. Get Your UserID
1. Login to [GetGrass.io](https://app.getgrass.io)
2. Press F12 to open Developer Console
3. Type and enter:
   ```js
   allow pasting
   ```
4. Then enter:
   ```js
   localStorage.getItem('userId')
   ```
5. Copy your UserID (without the quotes)

### 2. Setup Bot
1. Clone the repository:
   ```bash
   git clone https://github.com/scindo07/getgrass.git
   cd getgrass
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   

3. Install packages
   ```bash
   pip install -r requirements.txt
   ```


4. Create `uid.txt` with your user IDs:
   ```
   userId1
   userId2
   userId3
   ```

## Run bot
```bash
python main.py
```

The script will:
- Automatically manage and rotate proxies
- Move failed proxies to `error-proxy.txt`
- Assign new working proxies as needed

## Notes
- Automatically detect how many proxies and will divide all the proxies for all the accounts.
- You can run this bot at your own risk, I'm not responsible for any loss or damage caused by this bot.
- This bot is for educational purposes only.

## Credits and Acknowledgments
Special thanks to:
- [im-hanzou](https://github.com/im-hanzou) - For the inspiration and original concept
- [cmalf](https://github.com/cmalf) - For inspiration and contributions to the project

This project builds upon their work to create an enhanced multi-account farming solution for GetGrass.io.
