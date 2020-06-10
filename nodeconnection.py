#Developer: Curly60e
#PyBLOCK its a clock of the Bitcoin blockchain.
#Version: 0.4.0

import base64, codecs, json, requests
import pickle
import os
import os.path
import qrcode
import time as t
from pblogo import *

lndconnectload = {"ip_port":"", "tls":"", "macaroon":"", "lncli":""}

def clear(): # clear the screen
    os.system('cls' if os.name=='nt' else 'clear')

if os.path.isfile('blndconnect.conf'): # Check if the file 'bclock.conf' is in the same folder
    lndconnectData= pickle.load(open("blndconnect.conf", "rb")) # Load the file 'bclock.conf'
    lndconnectload = lndconnectData # Copy the variable pathv to 'path'
else:
    clear()
    blogo()
    print("\n\tIf you are going to use your local node leave IP:PORT/CERT/MACAROONS in blank.\n")
    lndconnectload["ip_port"] = input("Insert IP:PORT to your node: ") # path to the bitcoin-cli
    lndconnectload["tls"] = input("Insert the path to tls.cert file: ")
    lndconnectload["macaroon"] = input("Insert the path to admin.macaroon: ")
    print("\n\tLocal Lightning Node connection.\n")
    lndconnectload["lncli"] = input("Insert the path to lncli: ")
    pickle.dump(lndconnectload, open("blndconnect.conf", "wb")) # Save the file 'bclock.conf'

def locallistchaintxns():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    lncli = " listchaintxns"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    n = d['transactions']
    while True:
        clear()
        print("\033[1;32;40m")
        blogo()
        print("\033[0;37;40m")
        print("<<< Back to the Main Menu Press Control + C.\n\n")
        print("\t\nTransactions\n")
        try:
            for r in range(len(n)):
                s = n[r]
                print("Transaction Hash: " + s['tx_hash'])
            nd = input("\nSelect RHash: ")

            for r in range(len(n)):
                s = n[r]
                nn = s['tx_hash']
                trx = s['dest_addresses']
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------------------")
                    print("""
                    Amount: {} sats
                    Tx Hash: {}
                    Block Hash: {}
                    Block Height: {}
                    Confirmations: {}
                    Destination: {}
                    """.format(s['amount'], s['tx_hash'], s['block_hash'], s['block_height'], s['num_confirmations'], trx))
                    print("----------------------------------------------------------------------------------------------------------------\n")
                    print("\nTransaction Hash")
                    print("\033[1;30;47m")
                    qr.add_data(s['tx_hash'])
                    qr.print_ascii()
                    print("\033[0;37;40m")
            input("\nContinue... ")
        except (KeyboardInterrupt, SystemExit):
            break

def locallistinvoices():
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    lncli = " listinvoices"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    n = d['invoices']
    while True:
        clear()
        print("\033[1;32;40m")
        blogo()
        print("\033[0;37;40m")
        print("<<< Back to the Main Menu Press Control + C.\n\n")
        print("\tInvoices\n")
        try:
            for r in range(len(n)):
                s = n[r]
                print("Invoice: " + s['r_hash'] + " " + s['state'])

            nd = input("\nSelect RHash: ")

            for r in range(len(n)):
                s = n[r]
                nn = s['r_hash']
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------------------")
                    print("""
                    Memo: {}
                    Invoice: {}
                    Amount: {} sats
                    State: {}
                    """.format(s['memo'], s['payment_request'], s['amt_paid_sat'], s['state']))
                    print("----------------------------------------------------------------------------------------------------------------\n")
                    print("\033[1;30;47m")
                    qr.add_data(s['payment_request'])
                    qr.print_ascii()
                    print("\033[0;37;40m")
            input("\nContinue... ")
        except (KeyboardInterrupt, SystemExit):
            break

def locallistchannels():
    lncli = " listchannels"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    n = d['channels']
    while True:
        clear()
        print("\033[1;32;40m")
        blogo()
        print("\033[0;37;40m")
        print("<<< Back to the Main Menu Press Control + C.\n\n")
        print("\t\nChannels\n")
        try:
            for r in range(len(n)):
                s = n[r]
                print("Node ID: " + s['remote_pubkey'])

            nd = input("\nSelect a Node ID: ")

            for r in range(len(n)):
                s = n[r]
                nn = s['remote_pubkey']
                if nd == nn:
                    print("\n----------------------------------------------------------------------------------------------------------------")
                    print("""
                    Active: {}
                    Node ID: {}
                    Channel Point: {}
                    Channel Capacity: {} sats
                    Local Balance: {} sats
                    Remote Balance: {} sats
                    Total Sent: {} sats
                    Total Received: {} sats
                    """.format(s['active'], s['remote_pubkey'], s['channel_point'], s['capacity'], s['local_balance'], s['remote_balance'], s['total_satoshis_sent'], s['total_satoshis_received']))
                    print("----------------------------------------------------------------------------------------------------------------\n")

            input("\nContinue... ")
        except (KeyboardInterrupt, SystemExit):
            break

def localgetinfo():
    lncli = " getinfo"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    print("\n----------------------------------------------------------------------------------------------------------------")
    print("""
    Version: {}
    Node ID: {}
    Alias: {}
    Color: {}
    Pending Channels: {}
    Active Channels: {}
    Inactive Channels: {}
    Peers: {}
    URLS: {}
    """.format(d['version'], d['identity_pubkey'], d['alias'], d['color'], d['num_pending_channels'], d['num_active_channels'], d['num_inactive_channels'], d['num_peers'], d['uris']))
    print("----------------------------------------------------------------------------------------------------------------\n")
    input("\nContinue... ")

def localaddinvoice():
    lncli = " addinvoice"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    amount = input("Amount in sats: ")
    memo = input("Memo: ")
    lsd = os.popen(lndconnectload['lncli'] + lncli + " --memo " + memo + "-PyBLOCK" + " --amt " + amount).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    print("\033[1;30;47m")
    qr.add_data(d['payment_request'])
    qr.print_ascii()
    print("\033[0;37;40m")
    print("Lightning Invoice: " + d['payment_request'])
    b = str(d['payment_request'])
    while True:
        lsd = os.popen(lndconnectload['lncli'] + " decodepayreq " + b).read()
        lsd0 = str(lsd)
        d = json.loads(lsd0)
        r = d['payment_hash']
        lsdn = os.popen(lndconnectload['lncli'] + " lookupinvoice " + r).read()
        lsdn0 = str(lsdn)
        n = json.loads(lsdn0)
        if n['state'] == 'SETTLED':
            print("\033[1;32;40m")
            clear()
            blogo()
            tick()
            print("\033[0;37;40m")
            t.sleep(2)
            break
        elif n['state'] == 'CANCELED':
            print("\033[1;31;40m")
            clear()
            blogo()
            canceled()
            print("\033[0;37;40m")
            t.sleep(2)
            break

def localpayinvoice():
    invoice = input("Insert Invoice: ")
    lncli = " payinvoice "
    lsd = os.popen(lndconnectload['lncli'] + " decodepayreq " + invoice).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    if d['num_satoshis'] == "0":
        amt = " --amt "
        amount =  input("Amount in satoshis: ")
        os.system(lndconnectload['lncli'] + lncli + invoice + amt + amount)
        t.sleep(2)
    else:
        os.system(lndconnectload['lncli'] + lncli + invoice )
        t.sleep(2)

def localgetnetworkinfo():
    lncli = " getnetworkinfo"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    print("\n----------------------------------------------------------------------------------------------------------------")
    print("""
    Numbers of Nodes: {}
    Numbers of Channels: {}
    Total Network Capacity: {} sats
    Average Channel Size: {}
    Minimum Channel Size: {}
    Maximum Channel Size: {}
    Median Channel Size: {} sats
    Zombie channels: {}
    """.format(d['num_nodes'], d['num_channels'], d['total_network_capacity'], d['avg_channel_size'], d['min_channel_size'], d['max_channel_size'], d['median_channel_size_sat'], d['num_zombie_chans']))
    print("----------------------------------------------------------------------------------------------------------------\n")
    input("\nContinue... ")

def localkeysend():
    print("\n\tYou ar going to send a payment using KeySend - Note: You don't need any invoice, just your peer ID.")
    lncli = " sendpayment "
    node = input("Send to NodeID: ")
    amount = input("Amount in sats: ")
    while True:
        if amount == "" or amount == "0":
            amount = input("\nAmount in sats: ")
        else:
            break
    os.system(lndconnectload['lncli'] + lncli + "--keysend --d=" + node + " --amt=" + amount + " --final_cltv_delta=40")

def localchannelbalance():
    lncli = " channelbalance"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    print("\n----------------------------------------------------------------------------------------------------------------")
    print("""
    Balance: {} sats
    Pending Channels: {} sats
    """.format(d['balance'], d['pending_open_balance']))
    print("----------------------------------------------------------------------------------------------------------------\n")
    input("\nContinue... ")

def localnewaddress():
    lncli = " newaddress p2wkh"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    print("\033[1;30;47m")
    qr.add_data(d['address'])
    qr.print_ascii()
    print("\033[0;37;40m")
    print("Bitcoin Address: " + d['address'])
    input("\nContinue... ")

def localbalanceOC():
    lncli = " walletbalance"
    lsd = os.popen(lndconnectload['lncli'] + lncli).read()
    lsd0 = str(lsd)
    d = json.loads(lsd0)
    print("\n------------------------------------------------------------------------------------")
    print("Total Balance: " + d['total_balance'] + " sats")
    print("Confirmed Balance: " + d['confirmed_balance'] + " sats")
    print("Unconfirmed Balance: " + d['unconfirmed_balance'] + " sats")
    print("------------------------------------------------------------------------------------\n")
    input("\nContinue... ")

# Remote connection with rest -------------------------------------

def getnewinvoice():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    amount = input("Amount in sats: ")
    memo = input("Memo: ")
    url = 'https://{}/v1/invoices'.format(lndconnectload["ip_port"])
    data = {

        }
    if amount == "":
        r = requests.post(
                url,
                headers=headers, verify=cert_path,
                json={"memo": memo + " -PyBLOCK"},
            )
    else:
        r = requests.post(
                url,
                headers=headers, verify=cert_path,
                json={"value": amount, "memo": memo + " -PyBLOCK"},
            )

    a = r.json()
    print("\033[1;30;47m")
    qr.add_data(a['payment_request'])
    qr.print_ascii()
    print("\033[0;37;40m")
    print("Lightning Invoice: " + a['payment_request'])
    b = str(a['payment_request'])
    while True:
        url = 'https://{}/v1/payreq/{}'.format(lndconnectload["ip_port"], b)
        r = requests.get(url, headers=headers, verify=cert_path)
        a = r.json()
        url = 'https://{}/v1/invoice/{}'.format(lndconnectload["ip_port"],a['payment_hash'])
        rr = requests.get(url, headers=headers, verify=cert_path)
        m = rr.json()
        if m['state'] == 'SETTLED':
            print("\033[1;32;40m")
            clear()
            blogo()
            tick()
            print("\033[0;37;40m")
            t.sleep(2)
            break
        elif m['state'] == 'CANCELED':
            print("\033[1;31;40m")
            clear()
            blogo()
            canceled()
            print("\033[0;37;40m")
            t.sleep(2)
            break

def payinvoice():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    while True:
        bolt11 = input("Insert the invoice to pay: ")
        r = requests.post(
            url='https://{}/v1/channels/transactions'.format(lndconnectload["ip_port"]), headers=headers, verify=cert_path, json={"payment_request": bolt11}
        )
        try:
            r.json()['error']
            print("\nThe Invoice don't have an amount. Please insert an Invoice with amount. \n")
            continue
        except:
            break
    ok, checking_id, fee_msat, error_message = r.ok, None, 0, None
    r = requests.get(url='https://{}/v1/payreq/{}'.format(lndconnectload["ip_port"],bolt11), headers=headers, verify=cert_path,)
    t.sleep(5)
    if r.ok:
        checking_id = r.json()["payment_hash"]
        print("\033[1;32;40m")
        clear()
        blogo()
        tick()
        print("\033[0;37;40m")
        t.sleep(2)
    else:
        error_message = r.json()["error"]
        print("\033[1;31;40m")
        clear()
        blogo()
        canceled()
        print("\033[0;37;40m")
        t.sleep(2)

def decodepayment():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    dcd = input("Invoice: ")
    url = 'https://{}/v1/payreq/{}'.format(lndconnectload["ip_port"], dcd)
    r = requests.get(url, headers=headers, verify=cert_path)
    print(r.json())

def getnewaddress():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    url = 'https://{}/v1/newaddress'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    addr = r.json()
    print("\033[1;30;47m")
    qr.add_data(addr['address'])
    qr.print_ascii()
    print("\033[0;37;40m")
    print("Bitcoin Address: " + addr['address'])
    input("\nContinue... ")

def listchaintxns():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/transactions'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    a = r.json()
    b = str(a)
    c = b.split(',')
    d = c
    for d in c:
        print(d)
    t.sleep(10)

def listinvoice():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/invoices'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    a = r.json()
    b = str(a)
    c = b.split(',')
    d = c
    for d in c:
        print(d)
    input("\nContinue... ")

def invoicesettle():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    invoice = input("Insert the invoice: ")
    while True:
        url = 'https://{}/v1/payreq/{}'.format(lndconnectload["ip_port"], invoice)
        r = requests.get(url, headers=headers, verify=cert_path)
        a = r.json()
        url = 'https://{}/v1/invoice/{}'.format(lndconnectload["ip_port"],a['payment_hash'])
        rr = requests.get(url, headers=headers, verify=cert_path)
        m = rr.json()
        if m['state'] == 'SETTLED':
            print("\033[1;32;40m")
            clear()
            blogo()
            tick()
            print("\033[0;37;40m")
            t.sleep(2)
            break
        elif m['state'] == 'CANCELED':
            print("\033[1;31;40m")
            clear()
            blogo()
            canceled()
            print("\033[0;37;40m")
            t.sleep(2)
            break

def getinfo():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    a = r.json()
    print("\n----------------------------------------------------------------------------------------------------------------")
    print("""
    Version: {}
    Node ID: {}
    Alias: {}
    Color: {}
    Pending Channels: {}
    Active Channels: {}
    Inactive Channels: {}
    Peers: {}
    URLS: {}
    """.format(a['version'], a['identity_pubkey'], a['alias'], a['color'], a['num_pending_channels'], a['num_active_channels'], a['num_inactive_channels'], a['num_peers'], a['uris']))
    print("----------------------------------------------------------------------------------------------------------------\n")
    input("\nContinue... ")

def channels():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/channels'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    a = r.json()
    b = str(a)
    c = b.split(',')
    d = c
    for d in c:
        print(d)
    input("\nContinue... ")

def channelbalance():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/balance/channels'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    a = r.json()
    print("\n----------------------------------------------------------------------------------------------------------------")
    print("""
    Balance: {} sats
    Pending Channels: {} sats
    """.format(a['balance'], a['pending_open_balance']))
    print("----------------------------------------------------------------------------------------------------------------\n")
    input("\nContinue... ")


def balanceOC():
    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/balance/blockchain'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    a = r.json()
    print("\n------------------------------------------------------------------------------------")
    print("Total Balance: " + a['total_balance'] + " sats")
    print("Confirmed Balance: " + a['confirmed_balance'] + " sats")
    print("Unconfirmed Balance: " + a['unconfirmed_balance'] + " sats")
    print("------------------------------------------------------------------------------------\n")
    input("\nContinue... ")


# END Remote connection with rest -------------------------------------
