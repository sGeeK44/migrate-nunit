import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_files(directory):
    cs_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                cs_files.append(os.path.join(root, file))
    return cs_files


def read_file(file_path: str):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def write_file(file_path: str, content:str):
    with open(file_path, 'w') as file:
        file.write(content)


def convert(nunit: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Convert NUnit test to XUnit test. Response should constains only code without any additionnal comment of your work inside and no markdown format. Dont forget to add new line at the end of file to be compliant with git."},
            {
                "role": "user",
                "content": nunit}
        ]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert NUnit tests style to XUnit style.")
    parser.add_argument("dir", help="Root UnitTest directory path.")
    args = parser.parse_args()

    try:
        print("Starting conversions")
        client = OpenAI()
        for cs_file in get_files(args.dir):
            print(f"Convert {cs_file}")
            nunit = read_file(cs_file)
            xunit = convert(nunit)
            write_file(cs_file, xunit)
            print(f"Done.")
    except Exception as e:
        print(f"Fatal: {e}")
