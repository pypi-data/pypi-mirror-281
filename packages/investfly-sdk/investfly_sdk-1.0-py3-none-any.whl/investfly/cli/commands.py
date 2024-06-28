import argparse
import pickle
import os.path

from investfly.cli.CliApiClient import CliApiClient

def main():
    # Check to see if user already has a session active
    if os.path.exists('/tmp/loginSession'):
        tmpfile = open('/tmp/loginSession', 'rb')
        restApi = pickle.load(tmpfile)
        tmpfile.close()
    else:
        restApi = CliApiClient("https://api.investfly.com")

    # CLI Commands
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    parser_login = subparser.add_parser('login', help='Login to Investfly')
    parser_login.add_argument('-u', '--username', required='true', help='Input username')
    parser_login.add_argument('-p', '--password', required='true', help='Input user password')

    subparser.add_parser('whoami', help='View your user information')

    subparser.add_parser('logout', help='Logout')

    parser_strategy = subparser.add_parser('strategy', help='View all your current strategies')
    parser_strategy.add_argument('-id', help='Provide the Strategy ID')
    parser_strategy.add_argument('-o', '--output-file', help='Provide a location to save the output file of a custom strategy (Requires Strategy ID)')
    parser_strategy.add_argument('-u', '--update-file', help='Provide the file location to update the script of a custom strategy (Requires Strategy ID)')

    args = parser.parse_args()

    # If user is logging in, create a new login session and save it locally
    if args.command == 'login':
        restApi.login(args.username, args.password)
        tmpFile = open('/tmp/loginSession', 'ab')
        pickle.dump(restApi, tmpFile)
        tmpFile.close()

    elif args.command == 'logout':
        restApi.logout()
        os.remove('/tmp/loginSession')

    elif args.command == 'whoami':
        restApi.getStatus()

    elif args.command == 'strategy':
        if all(e is None for e in [args.id, args.output_file, args.update_file]):
            restApi.getStrategies()
        elif (args.output_file is not None) and (args.id is not None):
            try:
                code = restApi.saveStrategy(args.id)
                file = open(args.output_file, "w")
                file.write(code)
                file.close()
                print('File successfully saved to '+args.output_file)
            except Exception as e:
                print(e)
        elif (args.update_file is not None) and (args.id is not None):
            try:
                file = open(args.update_file, "r")
                code = file.read()
                restApi.updateStrategy(args.id, code)
                file.close()
            except Exception as e:
                print(e)
        else:
            parser_strategy.print_help()


    else:
        parser.print_help()


if __name__ == '__main__':
    main()