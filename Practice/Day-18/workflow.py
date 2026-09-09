def show_workflow():

    workflow = """

USER
 |
 v
Receive Query
 |
 v
Understand Intent
 |
 v
Planning Module
 |
 v
Select Tool
 |
 +------------+
 |            |
 v            v
Document    Calculator
Search
 |
 v
Analyze Data
 |
 v
Generate Response
 |
 v
USER


"""

    print(workflow)



if __name__ == "__main__":
    show_workflow()