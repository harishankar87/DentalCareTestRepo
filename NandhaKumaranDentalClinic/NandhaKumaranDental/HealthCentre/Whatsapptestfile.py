from WPP_Whatsapp import Create
import psutil

def whatsappApi(whatsappNumber):
    
    
    # for pc in psutil.process_iter():
    #     try:
    #         print(pc.cmdline())
    #     except psutil.AccessDenied:
    #         continue
        
    # start client with your session name
    your_session_name = "test"
    creator = Create(session=your_session_name)
    # client = creator.start()
    client = creator.start()
    # Now scan Whatsapp Qrcode in browser

    # check state of login
    if creator.state != 'CONNECTED':
        raise Exception(creator.state)

    phone_number = whatsappNumber # or "+201016708170"
    message = '''Hello From WPP WhatsApp Test Code !
    A reminder from Dr Nandha kumar Dental clinic. Your Appointment has been fixed on 12 July 23 at 6pm and Don't forget your prescription!! '''

    # Simple message
    result = client.sendText(phone_number, message)

    chrome_process = psutil.Process(1300)
    info = chrome_process.info()
    print(info)

# if __name__ == "__main__":
    # whatsappApi("+919444205002")

