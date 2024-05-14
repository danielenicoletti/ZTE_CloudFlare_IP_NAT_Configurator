# ZTE CLOUDFLARE IP NAT CONFIGURATOR

This tool is designed to connect to a ZTE H2640W router and open the ports indicated in the [Cloudflare IP Ranges](https://www.cloudflare.com/ips/) page.

## How to install it

1. Git clone this repo
2. Open a shell in the folder
3. Install requirements
   - `pip -r requirements.txt` on windows
   - `pip3 -r requirements.txt` on linux (usually)

## How to use it

1. Login into your router
2. Go into Internet -> Security -> Port Forwarding
3. Press F12 to show the browser developer option
4. Go into the `Network` tab
5. Edit any rules (like putting it off)

From here you will be able to find the packet sent to the router to edit the rule.

You must take note of:

- SID, located under `Cookie` in the `Header`
  ![](https://github.com/danielenicoletti/ZTE_CloudFlare_IP_NAT_Configurator/blob/main/imgs/SID.png?raw=true)
- sessionTOKEN, located under the `Payload`
  ![](https://github.com/danielenicoletti/ZTE_CloudFlare_IP_NAT_Configurator/blob/main/imgs/SESSION%20TOKEN.png?raw=true)

You can now run the script using `python main.py` on windows or `python3 main.py` on linux

You will be asked to add:

- the router IP
- the internal client that needs to expose the port (aka the server)
- the port
- a name
- the SID (you obtained before)
- the SESSION_TOKEN (you obtained before)

Please note that the sessionTOKEN changes after a few minutes so you must be pretty fast. (I wasn't able to understand how it works)
