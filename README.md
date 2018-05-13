I use a spreadsheet to keep track of frequent flyer miles accrued over the
course of the year. I have the distances between the most common origins and
destinations, but I'm constantly going online to look up distances I don't know
off-hand. I've found sources on line for calculating the distances, but they've
often been slow, awkward, or otherwise clumsy to interface with. In order to
make my life simpler, I decided to write a Python script to automate the query
and scrape the results.

Carrying this a bit further, I thought it would be nice if the spreadsheet
could interface with the web scraper directly. It would be overkill to turn the
scraper into an always-on API, but it seemed like a good opportunity to
experiment with some AWS services that facilitate the serverless craze.
Specifically, it gave me an opportunity to play with
[Lambda](https://aws.amazon.com/lambda) and
[API Gateway](https://aws.amazon.com/api-gateway).

The web scraper it self is called `WebFlyer` as it fetches data from the
[WebFlyer mileage calculator](http://www.webflyer.com/travel/mileage_calculator).
Under the hood, the scraper depends on
[Requests](http://docs.python-requests.org/en/master/) to fetch the data and
[lxml](http://lxml.de/) to parse the results. (NB: This mileage calculator has
a few quirks, such as rounding results to three significant digits, so results
can vary from reality.)

The file `lambda_function.py` contains the handler used to mediate between
Lambda and API Gateway by converting API path parameters into arguments to
`WebFlyer`.

Because the scraper depends on extra libraries that are not part of the
standard library available to Lambda functions written in Python, these
dependencies must be packaged up with the actual code and uploaded to AWS as a
ZIP file. To rebuild the ZIP file run the following:

```bash
$ zip -f -r get_mileage.zip lambda_function.py web_flyer.py chardet certifi idna urllib3 requests lxml -x */__pycache__/ *.pyc
```

To upload the code to Lambda:

```bash
$ aws lambda update-function-code --function-name get_mileage --zip-file fileb://get_mileage.zip
```

(TODO: Describe API Gateway integration.)
