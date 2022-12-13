# HAss-TM-Integrations

This repository contains some Integration developed to validate a Threat Model proposed to SpliTech 2022.

If you want more information about this work, you can read the paper in one of the following repositories:
- [Politecnico di Torino](https://iris.polito.it/handle/11583/2963822)
- [Research Gate](https://www.researchgate.net/publication/360627814_A_Threat_Model_for_Extensible_Smart_Home_Gateways)
- [IEEE Xplore](https://ieeexplore.ieee.org/document/9854235)

You can also find a recorded presentation on [YouTube](https://www.youtube.com/watch?v=Hczqbm3rWSE) and the slide of the conference's presentation on [Slide Share](https://www.slideshare.net/LucaMannella/a-threat-model-for-extensible-smart-home-gateways).


## Cite the paper

For citing the paper you can import the following BibTex:

``` Bibtex
@inproceedings{CornoMannella2022ThreatModel,
  title={A Threat Model for Extensible Smart Home Gateways},
  author={Corno, Fulvio and Mannella, Luca},
  booktitle={2022 7th International Conference on Smart and Sustainable Technologies (SpliTech)},
  pages={1-6},
  year={2022}, month={July},
  organization={IEEE},
  keywords={Cybersecurity, Gateways, Home Assistant, Internet of Things, Threat Modeling, Smart Home},
  doi={10.23919/SpliTech55088.2022.9854235}
}
```

### Paper Abstract 

This paper proposes a threat model for a specific class of components of IoT infrastructures: smart home gateways extensible through plug-ins. 
The purpose of the proposed model is twofold. From one side, it helps to understand some possible issues that could be generated from a malicious or defective implementation of a plug-in and affect the gateway itself or other smart home devices. Consequently, the model could help programmers of gateway applications, plug-ins, and devices think about possible countermeasures and develop more resilient solutions. On the other side, the model could be regarded as a set of guidelines. Indeed, plug-in developers should not create plug-ins acting like the threats reported in the paper.
To provide a first validation of the model, the paper presents a use case based on Home Assistant, an open-source smart home gateway application.


## Available components

### ``switch_target``

As the name suggests, the ``switch_target`` is targeted by the other two integrations.
It represents a fake switch with two possible states: *on* and *off*.
In addition, this integration contains a *secret value* that will be altered by the ``light_altering_state``.
This value (in a proper integration) should remain private (i.e., it should be used only by the integration itself).

### Two Integrations targeting the ``switch_target``

The other two integrations (``light_simple_access`` and ``light_altering_state``) are designed to emulate the managements of two different lights.
They have a *brightness value* and two possible states: *on* and *off*.
They behave like lights with additional malicious characteristics. Indeed, both these integrations are able to modify the status and the private data of the switch target, an integration outside their scope.

#### ``light_simple_access``

The first light is used to demonstrate some threats reported in the previously cited threat model (specifically T3, T7, T9, and T11).

When it is turned on in the front-end dashboard, the integration gets a reference to the ``switch_target`` to access its secret value (a piece of information outside its scope).
This behavior could lead to T1 or T2 according to what the malicious developer desires to do with the stolen data. 
Indeed, it could directly use the secret to access a private resource (e.g., if the secret is an access token) by materializing T1 or sending this information on a remote server (T2).

Furthermore, to exploit integrity (T4) and availability (T6) threats, when this light is turned off, ``light_simple_access`` modifies the ``switch_target``'s secret (T4).
If the target integration uses this variable to perform its tasks (e.g., it is an access token used to send power consumption data to a different dashboard), this change could also create a partial lack of availability (T6). I.e., the switch seems to work regularly, but a part of its functionalities is compromised.

#### ``light_altering_state``

The second light is used to demonstrate T1, T2, T4, and T6.

To materialize T3, every time a user turns on or off this light, the integration alters the ``switch_target``'s state — which is a state out of the integration’s scope.
If the switch is on, its state becomes off and vice versa (i.e., the switch is toggled).

Furthermore, the ``light_altering_state``also demonstrates T7. Indeed, even if the user is always able to change the state of the switch, the presented integration is partially in control of it, revealing an availability threat in the use case.

Indeed, invoking the toggle method directly from the reference to the ``switch_target`` integration, the platform could not detect who changed the device’s state (that seems to be changed by the original integration itself).
This action also demonstrates the feasibility of T9 and T11.
