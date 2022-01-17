


<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Stock Portfolio Tracker</h3>

  <p align="center">
    A portfolio tracking web application.
    <br />
    <a href="https://stockportfoliotracker.net">Visit Site</a>
    ·
    <a href="https://github.com/felixlevert/stock-tracker-app/issues">Report Bug</a>
    ·
    <a href="https://github.com/felixlevert/stock-tracker-app/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Stock Tracker App Screen Shot][product-screenshot]](https://stockportfoliotracker.net)

A simple web application that allows users to create an account, build their stock portfolio, and get live, to the second price update on some of the biggest stocks on the market. This was built as an learning experience, thus it uses the free tier of the Alpaca markets API, and is limited to 30 stocks at the moment.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Bulma](https://bulma.io/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Gunicorn](https://gunicorn.org/)
* [NGINX](https://www.nginx.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The development environment is containerized using Docker, and the setup is relatively simple.

First you'll need to install Docker and Docker-Compose
* Ubuntu
  ```sh
  apt-get install docker docker-compose
  ```
* Arch Linux
  ```sh
  pacman -S docker docker-compose
  ```
* Other - https://www.docker.com/

You will also need NPM
* Ubuntu
  ```sh
  apt-get install npm
  ```
* Arch Linux
  ```sh
  pacman -S npm
  ```
* Other - https://www.npmjs.com/


### Installation

1. Get a free API Key at [https://alpaca.markets/](https://alpaca.markets/)
2. Clone the repo
   ```sh
   git clone https://github.com/felixlevert/stock-tracker-app.git
   ```
3. Install NPM packages in the static folder
   ```sh
   cd services/web/src/static
   npm install
   ```
4. Create a .env.dev file in project root with the following values
   ```
    APP_SETTINGS=DevelopmentConfig
    DATABASE_URL=postgresql://stocks_dev:stocks_dev@db:5432/stocks_dev
    FLASK_APP=src/__init__.py
    FLASK_DEBUG=1
    SECRET_KEY=**ENTER A SECRET KEY HERE**
    ALPACA_API_KEY_ID=**ENTER YOUR ALPACA API KEY HERE**
    ALPACA_SECRET_KEY=**ENTER YOUR ALPACA SECRET KEY HERE**
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres
    APP_FOLDER=/usr/src/app
    ```
5. Build and run the docker containers
    ```sh
    docker-compose -f docker-compose.yml up -d --build
    ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- Add total values for each column of the portfolio table.
- Implement a detailed statistic page that shows various graphs of performance over time.

See the [open issues](https://github.com/felixlevert/stock-tracker-app/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Felix Levert - felix.levert@gmail.com

Project Link: [https://github.com/felixlevert/stock-tracker-app](https://github.com/felixlevert/stock-tracker-app)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/felixlevert/stock-tracker-app.svg?style=for-the-badge
[contributors-url]: https://github.com/felixlevert/stock-tracker-app/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/felixlevert/stock-tracker-app.svg?style=for-the-badge
[forks-url]: https://github.com/felixlevert/stock-tracker-app/network/members
[stars-shield]: https://img.shields.io/github/stars/felixlevert/stock-tracker-app.svg?style=for-the-badge
[stars-url]: https://github.com/felixlevert/stock-tracker-app/stargazers
[issues-shield]: https://img.shields.io/github/issues/felixlevert/stock-tracker-app.svg?style=for-the-badge
[issues-url]: https://github.com/felixlevert/stock-tracker-app/issues
[license-shield]: https://img.shields.io/github/license/felixlevert/stock-tracker-app.svg?style=for-the-badge
[license-url]: https://github.com/felixlevert/stock-tracker-app/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/felix-levert-179a811aa/
[product-screenshot]: ./images/product-screenshot.png