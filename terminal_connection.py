import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--figure", type=str,
                    help="Argument induces function which creates graphic",
                    action="store")
parser.add_argument("-nx", "--name_x", type=str,
                    help="Argument induces function which create x axis signature",
                    action="store")
parser.add_argument("-ny", "--name_y", type=str,
                    help="Argument induces function which create y axis signature",
                    action="store")
parser.add_argument("-s", "--sigma", help="Argument induces function which counts the error",
                    action="store_true")
args = parser.parse_args()


if args.figure:
    print(args.figure)

if args.sigma:
    pass

if args.name_x:
    print(args.name_x)

if args.name_y:
    print(args.name_y)

