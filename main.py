import argparse, json, subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Running tests in different browsers.")
    parser.add_argument('browsers', type=str, help="Browsers name list separated by commas")
    parser.add_argument('feature_file', type=str, help="Path of the .feature file or tag")
    return parser.parse_args()

def main():
    args = parse_args()
    browsers = args.browsers.split(',')
    feature_file = args.feature_file
    tag = False

    with open('configuration.json') as file:
        data = json.load(file)

    with open("REPORT.log", 'a+') as file:
        file.truncate(0)

    if ".feature" not in feature_file:
        tag = True

    for browser in browsers:
        if browser in data['browsers_enum']:
            if not tag:
                command = ["behave", f"-D", f"BROWSER={browser}", feature_file]
            else:
                command = ["behave", f"-D", f"BROWSER={browser}", "-t", feature_file]

            print(f"Running test in {browser}...")
            try:
                subprocess.run(command, shell=False, check=True)
            except subprocess.CalledProcessError as e:
                print("\nThe error happened when this command was running:", " ".join(e.cmd))
                exit(-1)
        else:
            print(f"The value '{browser}' does not match the possible browsers. See README file.")

if __name__ == "__main__":
    main()
