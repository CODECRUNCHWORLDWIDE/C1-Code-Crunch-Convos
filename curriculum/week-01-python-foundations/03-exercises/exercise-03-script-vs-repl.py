"""exercise-03-script-vs-repl.py

Goal
----
Compare what happens when you run a Python file two different ways:

1. ``python exercise-03-script-vs-repl.py``         (plain script mode)
2. ``python -i exercise-03-script-vs-repl.py``      (script, then REPL)

Tasks
-----
A. Modify the body of ``main()`` so that the script prints **three** lines
   when you run it. They can be anything you like — for example, a line
   greeting yourself, a line showing today's lecture number, and a line
   showing the value of ``answer`` (defined below).

B. Save the file, then run it both ways:

   .. code-block:: bash

       python exercise-03-script-vs-repl.py
       python -i exercise-03-script-vs-repl.py

C. Fill in the "Observations" section at the bottom of this file as
   triple-quoted comments. Compare the two runs:

   * Did the three lines print in both cases? (Yes/No)
   * After the script finished, did Python exit or drop into a ``>>>``
     prompt?
   * In the ``-i`` run, can you type ``answer`` at the prompt and see its
     value? Why or why not?

Estimated time
--------------
About 15 minutes.

Hints
-----
* ``-i`` is short for "interactive". It keeps the interpreter alive after
  the script ends, with all of the script's variables already defined.
* Exit the ``-i`` session with ``exit()`` or Ctrl+D.
"""

# A module-level variable. After the script runs, the REPL (in ``-i``
# mode) will have this name available.
answer: int = 42


def main() -> None:
    """Print three lines. Modify this function as part of task A."""
    # TODO (task A): replace the line below with three ``print(...)``
    # calls of your own choosing.
    print("Replace me with three of your own print() calls.")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------
# Observations (task C)
# ---------------------------------------------------------------------
# Replace the placeholder text inside the triple-quoted string below with
# your own notes after you have run the file both ways.

"""
Observations
------------
1. With ``python exercise-03-script-vs-repl.py`` I saw:
   <your notes here>

2. With ``python -i exercise-03-script-vs-repl.py`` I saw:
   <your notes here>

3. Typing ``answer`` at the ``>>>`` prompt after ``-i`` produced:
   <your notes here>

4. Summary of the difference between the two run modes:
   <your notes here>
"""
