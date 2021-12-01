# ACMA DQN Server
This project collaborates with [ACMA][1] to run smart refactoring agents. For this purpose, you must run this server on `localhost:5000`.

### How to run
After cloning the project, go to the directory of the project and add a new python virtual environment, then install its requirements:
> pip install -r requirements.txt

Then run the server (on the default address which is `localhost:5000`):
> flask run

There's 4 pre-trained models which you can use for refactoring: `model_1` to `model_4`.
To use one of pretrained models, go to address `localhost:5000` via a web-browser, you must see a swagger panel. Then in the swagger panel, click on `/load_weights/` then click on `Try it out` button and change the `string` to the name of a model. for example:
```
{
  "model_name": "model_1"
}
```
And then in below, click on `execute` button. It must response that the weights loaded successfuly. Then you can refactor your software, using `Accountant Agent` or `Gmabler Accountant Agent` in the [ACMA][1].

  [1]:https://github.com/hrahmadi71/a-cma
