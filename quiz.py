from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb-D4yl7mAabrP0jg1IivF8yocPE4TEMJjbTZ0cNQZ72SIMAlJuB_Jff-qyxcwg_bWoqH3vkuwJs3uyGsrvgH_laZsUAX3u8WWt_BfdOWmFXsJSr3HUZIBUnJyWVlMPr1W6nCdbbXZ_NUlSfyUWSJfLvC1pYXtNu-SUvui870nlmjyrD0QnrYKpn0sjIbW2UTCNHPL'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()