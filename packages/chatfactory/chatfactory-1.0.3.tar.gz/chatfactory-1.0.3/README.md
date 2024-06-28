## ChatFactory <img src="https://revivegretel.com/docs/_static/logo.png" width="20%"> 
ChatFactory is a library for automatically generating chats/dialogues grounded in a textual environment. The library can generate unlimited data to feed your chatbot model. 

The dialogues are generated using preprogrammed templates. The templates are Python functions that have parameters like the dialogue participants, their policies, and the dialogue's goal. Each policy determines the participant's responses based on context.

The library comes with a set of templates that can be immediately used to generate new [dialogues](#the-dialogues). Additionally, our library provides the tools needed to develop new templates. Please check our [notebook](template_tutorial.ipynb) for an example of how to develop a new template.

In addition to the library, we introduce a [challenge](#the-challenge). 

## Installation
Using pip:

```bash
pip install chatfactory
```
This project requires the `en_core_web_sm` model for spaCy. It should be automatically installed during the first import. However, if you encounter any issues, you can manually install it using the following command:
```bash
python -m spacy download en_core_web_sm
```

## Dependencies

- Python 3.8 or greater
- djikstar
- file-read-backwards
- tqdm
- notebook
- ipywidgets
- spacy
- pyinflect
- torch (optional) for running the baseline


## Usage

For quickly generating and running a dialogue using the templates that we have already developed:

```python
from chatfactory import DialogueGenerator
import chatfactory.environments.easy as easy_env

easy_world = easy_env.build_world()
generator = DialogueGenerator(easy_world, "error.log", "context.log")
dialogue = generator.generate_dialogue()
dialogue.run()
for utter in dialogue.utterances:
    print (utter.to_string())
```
The error.log and context.log indicate where the errors and the context are flushed. Please add the full path where
you prefer to store them.

## The dialogues

We have developed templates that generate dialogues in which a user issues a request to an agent. The agent should fulfill the user's request by taking several steps. Our dialogues are interactive because we allow the agent to issue an action in the environment. The actions can be getting an item, opening a door, or issuing utterances using the action say. To simplify things, we use utterance and action interchangeably. Here is an example of two short dialogues:
 
 ```
Jim says : Ada close a static door metal entity .
Ada tries going north .
Ada goes north from the static well . Ada looks in the static place porch path . Ada sees the green apple and the red apple .
Ada tries going north .
Ada goes north from the static place porch path . Ada looks in the place big living room . Ada sees Ada , coco and the static metal door entity .
Ada tries closing the static metal door entity in the place big living room .
Ada closes the static metal door entity .


Otto says : Gretel, Is Ada's location in the kitchen ?
Gretel says : Ada's location is not in the kitchen .
```
 
Each time a user or an agent utters, the environment provides feedback (except when executing the action "say"). Therefore, we consider the environment as an additional dialogue participant. The agent utters until it reaches the goal or exceeds the maximum number of steps. The environment is multi-player, so there are multiple agents and users. Each player provides a response using a rule-based policy. During the training/evaluation of the machine learning model, the rule-based policy is replaced with the machine learning policy. The dialogue's goal remains rule-based and is determined based on the context.

The dialogues are continuous in time, and their course depends on the utterances from previous dialogues. Once the dialogues are over, they are added to the context. The context is a log containing all the actions and utterances the agents execute in the environment. As time progresses, the context gets larger, and the agent has to develop long-term memory to remember important facts about the environment's configuration. Furthermore, it has to develop logical reasoning to deduce information that is not explicitly stated in the context. Our user policies are simpler because the user issues just a single request and stops uttering.

When creating dialogue templates, you are not restricted to developing user-agent dialogues. Our library can be utilized to create any type of dialogue.

## The challenge

We challenge you to train a machine learning model to enable the main player, Gretel, to utter the correct sentences in our [dialogues](#the-dialogues). 

To get you started, we have developed the following notebooks that provide examples of how to train and evaluate the agent: [start.ipynb](start.ipynb) and [baseline.ipynb](baseline.ipynb)

Please see the section *The challenge* in our paper, where we outline the rules. We kindly ask you to report the metrics that we require. Our [leaderboard](https://revivegretel.com/leaderboard) also displays the metrics. You are welcome to report any additional metrics or any interesting findings.

If you have any questions or require assistance with the challenge, please feel free to open a new GitHub issue. We're happy to let you know that we provide [documentation](https://revivegretel.com/docs) of our code.


### Submitting your solution

To submit your solution, please open a new GitHub issue. Please provide a link to your repository and include a notebook describing your solution. We welcome any additional materials, such as a project report or paper.

The competition is not limited by time. However, the first competitor to reach more than 95% on all dialogue types in the testing environment will earn a special prize and recognition from our agency. The leaderboard is available [here](https://revivegretel.com/leaderboard).


## Contribute

### Developing new dialogue templates
Having dedicated substantial time to developing the ChatFactory, we found ourselves needing help to create all the necessary dialogue templates to reach our five-year milestone. We would greatly appreciate your assistance in developing the remaining templates. 

The templates we need are detailed in the *Milestone* section of our paper. However, if you're interested in creating templates that you believe are important but aren't listed, feel free to submit those too. We're open to including them in our next challenge. You can find examples of templates [here](https://revivegretel.com/docs/chatfactory.generation.html#module-chatfactory.generation.templates).

### Submitting your templates
To submit your dialogue templates, kindly create a new GitHub issue and include a link to your repository. Please document your code to help us and other developers better understand it. We also welcome any additional materials such as flow diagrams and a project report that further describe your templates and policies.

We will recognize the template developers for their contributions by featuring their new dialogue templates in our [Hall of Fame](https://revivegretel.com/hof). With your consent, we will include some of these templates in our next challenge. Six months from now, we'll spotlight one outstanding template and award a special prize to its creator. We encourage the development and submission of new templates because the users of ChatFactory will benefit from generating even more data for their models. Furthermore, through a collaborative effort, we can create the first logical agent.


Your efforts are greatly appreciated!

## Support us
Your generosity will bring our research closer to the next big milestone: an agent with the intelligence of a 10-year-old child.
We plan to use the donations to build the next challenge. In addition to research, we want to be the voice for the most vulnerable. Therefore, we plan to use 10% of the donations to provide medical care and shelter for stray animals. Your kindness will give them a chance to live.

We will also post updates about our progress and the impact of your donations.


You can also support us via:
- [buymeacoffee.com/agenthans](https://www.buymeacoffee.com/agenthans)
- BTC: `bc1q8e58n8a86p9yhvw3mt3ldqtnm2ypajssqu5wpg`
- Ethereum: `0x49Cd7ab7f2f7209fcCD8608cAfBCcD9012772669`
- Monero:  `4B1qU9xanShCieLmvKvmhraYovLVMeMfpF9yToj6BBiPRXWPnYjXiNiSovTZw1vZdwFc6J5GHwYFvbxeeS1eYRWJCbdSgFF`

We want to thank you for your support and belief in our mission!
