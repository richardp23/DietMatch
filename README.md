# DietMatch

An OpenAI-powered recipe generative for those with alternative diets.

## Requirements

* [Edamam API Access](https://www.edamam.com/)
* [OpenAI API Access](https://platform.openai.com/)

## Getting Started

Git clone this repository, then create a .env file with the following environment variables:

```
EDAMAM_APP_ID=""
EDAMAM_APP_KEY=""
OPENAI_KEY=""
```

Fill in each environment variables with the correct keys from your API (see [Requirements](#Requirements)).

To use the app in your terminal, run the following command:

```
python3 -m main.py
```

To use the app's web interface, run the following command:

```
python3 -m app.py
```

The default URL for the web interface is `localhost:3000`.
