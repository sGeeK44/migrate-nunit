import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

if __name__ == "__main__":    
    try:        
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Convert NUnit test to XUnit test. Response should constains only code without any additionnal comment of your work inside and no markdown format."},
                {
                    "role": "user",
                    "content": """
using Newtonsoft.Json;
using NFluent;
using NUnit.Framework;
using Zg.Lib.Serialization.Json;

namespace Zg.Api.UnitTests
{
    [TestFixture]
    public class ApiResponseTest
    {
        public JsonSerializer<APIResponse> JsonSerializer { get; private set; }

        [SetUp]
        public void SetUp()
        {
            JsonSerializer = new JsonSerializer<APIResponse>();

        }

        [TestCase("A")]
        [TestCase("B")]
        public void DeserializeFromApiStream(string x)
        {
            var json = "{\"error\":{\"code\":\""+ x + "\",\"message\":\"B\"},\"type\":\"C\",\"value\":\"D\",\"commands\":[{\"id\":1,\"name\":\"E\",\"arguments\":\"F\"}]}";

            var result = JsonSerializer.Deserialize(json);


            Check.That(result.Error.Code).IsEqualTo("A");
            Check.That(result.Error.Message).IsEqualTo("B");
            Check.That(result.Type).IsEqualTo("C");
            Check.That(result.Value).IsEqualTo("D");
            Check.That(result.Commands.Count).IsEqualTo(1);
            Check.That(result.Commands[0].Id).IsEqualTo(1);
            Check.That(result.Commands[0].Name).IsEqualTo("E");
            Check.That(result.Commands[0].Arguments).IsEqualTo("F");
        }

        [Test]
        public void ApiResultV4()
        {
            var json =
                "{\"created\": [90012, 90210, 90211, 90212], \"accepted\": [90213, 91726, 91741, 97958], \"errors\": []}";

            var results = JsonSerializer.Deserialize(json);

            Check.That(results.Error.Code).IsEqualTo("A");
            Check.That(results.Error.Message).IsEqualTo("B");
        }
    }
}
"""
                }
            ]
        )        
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
