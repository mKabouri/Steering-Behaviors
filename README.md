# Steering-Behaviors

### Motivation:
The project is inspired by the desire to simulate and visualize various steering behaviors. These behaviors are fundamental in game development, robotics, and AI.

### Description:
This project implements several steering behaviors in Python using the Pygame library. It visualizes behaviors such as Seek, Pursuit, Avoid Obstacles, Flocking, and Circuit navigation. Each behavior is encapsulated in its own class with a clear interface, allowing for easy expansion and modification.

I am really proud of circuit behavior with obstacle avoidance (see ./src/behaviors/circuit.py) and the flocking behavior (see ./src/behaviors/flock.py) and the environment in circuit case (./src/environment.py).

I treated the case of collision in circuit case (see handle_collisions method in environment.py) and group avoidance in flock case (see inter_group_avoidance in flock.py). 

I implemented all behaviors and the environement from scratch.

My goal is to implement a small library of steering behavior for simulations.

### Demonstration:
* Flocking behavior:

![Flocking Behavior Simulation](./flock_behavior.gif)

* Circuit behavior:

![Circuit Behavior Simulation](./circuit_behavior.gif)


### Commands:
To run simulation:
```
python3 src/run.py
```
This will run the simulation with circuit behavior.

For other behaviors:
```
python3 src/run.py -b behavior_name 
```

where behavior_name is one of the following implemented behaviors:
* "seek" for SeekParticule,
* "flee" for FleeParticule,
* "circuit" for CircuitBehavior
* "flock" for FlockingBehavior
* "random" for RandomBehavior

After running, you can use your mouse:
- `LEFT CLICK`: Add a particule.
- `RIGHT CLICK`: Add a target (Seek and Flee behaviors) or an obstacle (Circuit behavior).
- `Q KEY`: Quit the simulation.
- `RESTART BUTTON`: Click to reset the environment.

### Improvements:
- Adding more behaviors (see Greg Reynolds paper).

### Done:
1. **Random**: The particule moves randomly in the environment.
2. **Seek**: Enables particules to autonomously move towards a target point.
3. **Flee**: Avoid the target.
4. **Multi-Particules (Flocking)**: Simulates flocking behavior among groups of particules. The particles are grouped based on particule color criteria.
5. **Circuit**: Particules navigate through a predefined circuit, avoiding collisions with other particules and obstacles and following the path.

### Reference:
- [Craig Reynolds' Steering Behaviors](https://www.red3d.com/cwr/steer/gdc99/)
- [The Coding Train - Steering Behaviors](https://www.youtube.com/watch?v=fWqOdLI944M&ab_channel=TheCodingTrain)

### Contributing:
Contributions to the project are welcome. Whether you're improving existing behaviors, adding new ones, or enhancing the simulation environment.
