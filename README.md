# Grailed Automation Tool

The Grailed Automation Tool is a Dash web application that helps users find and track items on the popular designer and streetwear marketplace, Grailed so that they can make more informed purchases. It uses a combination of Selenium and Beautiful Soup to scrape the product price, shipping price, description, user rating, and URL for every single product that meets the user's search criteria and visualizes this information in a live, interactive dashboard. The app also allows the user to track the prices of up to 10 products with live updates every 5 minutes. Without a tool like this, the user would have to comb through the website and open a specific product's page to see things such as description, shipping price, and user rating as well as manually track its price. 

## Getting Started

Create an environment with virtualenv or conda.

Install dependencies in requirements. txt

```
pip install -r requirements.txt
```

Install chromedriver: http://chromedriver.chromium.org/
Open Grailed_Bot.py and put the file location of the chromedriver executable on your system in the quotes:

```
chromedriver = "Put file location of chromedriver executable here"
```

Launch the app.

```
python app.py
```


## Built With

* [Dash](https://plot.ly/dash/)
* [Selenium](https://www.seleniumhq.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

