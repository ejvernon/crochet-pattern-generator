from dataclasses import dataclass
from bakery import assert_equal
from drafter import *

set_website_title("Crochet Pattern Generator")
set_site_information(
    author="Emma Vernon",
    description="Allows user's to input crochet pattern details and recieve a generated crochet pattern",
    sources="Thanks to Cisc 106 Blockpy, Drafter and ChatGPT",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/ejvernon/https://github.com/ejvernon/crochet-pattern-generator"]
    )
hide_debug_information()
set_website_framed(False)

@dataclass
class CrochetInstructions:
    row: int
    complete_row_instructions: str
    
@dataclass
class SafetyEyes:
    size: int
    row: int
    has_safety_eyes: bool
    
@dataclass
class SpecialInstructions:
    safety_eyes: SafetyEyes
    stuffing: bool
    
@dataclass
class Pattern:
    hook_size: int
    yarn_name: str
    yarn_type: str
    
@dataclass
class State:
    total_instructions: list[CrochetInstructions]
    current_row: int
    special_instructions: SpecialInstructions
    pattern_details: Pattern
   
initial_test_state = State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))


@route
def index(state:State)->Page:
    return Page(state,[
        Header("Crochet Pattern Builder"),
        "What would you like to do?",
        Button("Add a Row","stitch_instructions"),
        Button("Update a Row","update_instructions"),
        Button("Delete a Row","delete_instructions"),
        Button("Insert Pattern Info","pattern_info"),
        Button("Insert Additional Instructions","additional_instructions"),
        Button("View Generated Instructions","final_crochet_instructions")
        ])
        
#initial version of index
assert_equal(index(initial_test_state),
             Page(initial_test_state,
                  [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))

#index with content
assert_equal(index(State([CrochetInstructions(1,"1 sc, 1 inc, repeat around")], 1,
                         SpecialInstructions(SafetyEyes(8,4,True),True),Pattern(0,"",""))),
             Page(State([CrochetInstructions(1,"1 sc, 1 inc, repeat around")],1,
                        SpecialInstructions(SafetyEyes(8,4,True),True),Pattern(0,"","")),
                  [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))




@route
def save_stitch_instructions(state:State, row:int,instructions:str)->Page:
    row_instructions = CrochetInstructions(row,instructions)
    state.total_instructions.append(row_instructions)
    state.current_row = row
    return index(state)
    
#updated state with save_stitch_instructions
assert_equal(save_stitch_instructions(State([],0,
    SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
    , 1, "1 sc 1 inc"),
Page(State([CrochetInstructions(1,"1 sc 1 inc")],1,
             SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))


@route
def stitch_instructions(state:State)->Page:
    return Page(state,[
        Header("Input Row/Stitch Details"),
        "What Row Are You Working On?",
        TextBox("row"),
        "Write This Row's Instructions",
        TextBox("instructions"),
        Button("Save","save_stitch_instructions"),
        Button("Back","index")
         ])

#initial stitch_instructions
assert_equal(stitch_instructions(initial_test_state),
    Page(initial_test_state,[
        Header("Input Row/Stitch Details"),
        "What Row Are You Working On?",
        TextBox("row"),
        "Write This Row's Instructions",
        TextBox("instructions"),
        Button("Save", "save_stitch_instructions"),
        Button("Back","index")
         ]))


@route
def save_additional_instructions(state:State, safety_eyes:bool, safety_eye_insert:int, safety_eye_size:int, stuffing:bool)-> Page:
    additional_details = SpecialInstructions(SafetyEyes(0,0,False),False)
    if safety_eyes:
        additional_details.safety_eyes.has_safety_eyes = True
        additional_details.safety_eyes.size = safety_eye_size
        additional_details.safety_eyes.row = safety_eye_insert
    if stuffing:
        additional_details.stuffing = True
    state.special_instructions = additional_details
    return index(state)
 
#Has safety eyes test
assert_equal(save_additional_instructions(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
    ,True,4,8,False), 
            Page(State([], 0,
            SpecialInstructions(SafetyEyes(8,4,True),False),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))

#Has stuffing test
assert_equal(save_additional_instructions(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
    
,False,0,0,True), 
            Page(State([], 0,
            SpecialInstructions(SafetyEyes(0,0,False),True),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))



@route
def additional_instructions(state:State)->Page:
    return Page(state,[
        Header("Input Any Additional Details"),
        "Did You Use Safety Eyes?",
        CheckBox("safety_eyes"),
        "Safety Eye Size in mm (Leave blank if not used)",
        TextBox("safety_eye_size"),
        "What Row Did You Add Your Eyes?",
        TextBox("safety_eye_insert"),
        "Did You Stuff Your Project?",
        CheckBox("stuffing"),
        Button("Save","save_additional_instructions"),
        Button("Back","index")
         ])

#initial additional_instructions
assert_equal(additional_instructions(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
    
),
    Page(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
    
,
        [Header("Input Any Additional Details"),
        "Did You Use Safety Eyes?",
        CheckBox("safety_eyes"),
        "Safety Eye Size in mm (Leave blank if not used)",
        TextBox("safety_eye_size"),
        "What Row Did You Add Your Eyes?",
        TextBox("safety_eye_insert"),
        "Did You Stuff Your Project?",
        CheckBox("stuffing"),
        Button("Save","save_additional_instructions"),
        Button("Back","index")]))
         


@route
def save_pattern_info(state:State, hook_size:int, yarn_brand:str, yarn_name:str)->Page:
    pattern = Pattern(hook_size,yarn_brand,yarn_name)
    state.pattern_details = pattern
    return index(state)

#update save_pattern_info
assert_equal(save_pattern_info(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
    
,7,"Yarnsmiths","Chenille Chunky"),
        Page(State([],0,
            SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(7,"Yarnsmiths","Chenille Chunky")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))
    

@route
def pattern_info(state:State)->Page:
    return Page(state,[
        Header("Input Pattern Details"),
        "Hook Size (mm)",
        TextBox("hook_size"),
        "Yarn Brand",
        TextBox("yarn_brand"),
        "Yarn Name",
        TextBox("yarn_name"),
        Button("Save","save_pattern_info"),
        Button("Back","index")
         ])

#initial pattern_info
assert_equal(pattern_info(initial_test_state),
    Page(initial_test_state,
        [Header("Input Pattern Details"),
        "Hook Size (mm)",
        TextBox("hook_size"),
        "Yarn Brand",
        TextBox("yarn_brand"),
        "Yarn Name",
        TextBox("yarn_name"),
        Button("Save","save_pattern_info"),
        Button("Back","index")]))



def final_additional_details(state:State)->str:
    final = ""
    if state.special_instructions.safety_eyes.has_safety_eyes == True and state.special_instructions.stuffing == True :
        final = "Place " + str(state.special_instructions.safety_eyes.size) + "mm " + "Safety Eyes in Row " + str(state.special_instructions.safety_eyes.row) + "\n" + "Stuff Project"
    elif state.special_instructions.safety_eyes.has_safety_eyes == True and state.special_instructions.stuffing == False :
        final = "Place " + str(state.special_instructions.safety_eyes.size) + "mm "+ "Safety Eyes in Row " + str(state.special_instructions.safety_eyes.row)
    elif state.special_instructions.safety_eyes.has_safety_eyes == False and state.special_instructions.stuffing == True :
        final = str("Stuff Project")
    else:
        final = ""
    return final

#final_additional_details test 1: Eyes & Stuffing
assert_equal(final_additional_details(State([],0,SpecialInstructions(SafetyEyes(8,4,True),True), Pattern(0,"","")))
             ,"Place 8mm Safety Eyes in Row 4 \n Stuff Project")
#final_additional_details test 2: Eyes & No Stuffing
assert_equal(final_additional_details(State([],0,SpecialInstructions(SafetyEyes(8,4,True),False), Pattern(0,"","")))
             ,"Place 8mm Safety Eyes in Row 4")
#final_additional_details test 3: No Eyes but Stuffing
assert_equal(final_additional_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),True), Pattern(0,"","")))
             ,"Stuff Project")
#final_additional_details test 4: No Eyes or Stuffing
assert_equal(final_additional_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False), Pattern(0,"","")))
             ,"")


def final_pattern_details(state:State)->str:
    final = ""
    if state.pattern_details.hook_size != 0:
        final = "Hook size: " + str(state.pattern_details.hook_size) + " mm"
    if state.pattern_details.yarn_type != "" or state.pattern_details.yarn_name != "":
        final = final + " " + "\n" + " Yarn Used: " + state.pattern_details.yarn_name + " " + state.pattern_details.yarn_type      
    return final
 
#final_pattern_details test 1: Hook Size, Yarn Type & Yarn Name
assert_equal(final_pattern_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(7,"Yarnsmiths","Chenille Chunky"))),"Hook Size: 7 mm \n Yarn Used: Yarnsmiths Chenille Chunky")

#final_pattern_details test 2: Yarn Type & Yarn Name
assert_equal(final_pattern_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"Yarnsmiths","Chenille Chunky"))),"Yarn Used: Yarnsmiths Chenille Chunky")

#final_pattern_details test 3: Hook Size & Yarn Yype
assert_equal(final_pattern_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(7,"","Chenille Chunky"))),"Hook Size: 7 mm \n Yarn Used:  Chenille Chunky")

#final_pattern_details test 4: Hook Size & Yarn Name
assert_equal(final_pattern_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(7,"Yarnsmiths",""))),"Hook Size: 7 mm \n Yarn Used: Yarnsmiths ")

#final_pattern_details test 5: No Additional Details
assert_equal(final_pattern_details(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))),"")


def final_instructions(state:State)->str:
    total = ""
    for instructions in state.total_instructions:
        total = total + "Row " + str(instructions.row) + ": " + instructions.complete_row_instructions + "\n"
    return total

crochet_instructions_test1 = State([CrochetInstructions(1,"6 sc in mr"),CrochetInstructions(2,"6 inc"),CrochetInstructions(3,"1 inc, 1 sc")],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
crochet_instructions_test2 = State([CrochetInstructions(1,"6 sc in mr"),CrochetInstructions(2,"6 inc")],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
crochet_instructions_test3 = State([CrochetInstructions(1,"6 sc in mr")],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
crochet_instructions_test4 = State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))
  

#final_instructions test 1
assert_equal(final_instructions(crochet_instructions_test1),"Row 1: 6 sc in mr\nRow 2: 6 inc\nRow 3: 1 inc, 1 sc\n")

#final_instructions test 2
assert_equal(final_instructions(crochet_instructions_test2),"Row 1: 6 sc in mr\nRow 2: 6 inc\n")

#final_instructions test 3
assert_equal(final_instructions(crochet_instructions_test3),"Row 1: 6 sc in mr\n")

#final_instructions test 4
assert_equal(final_instructions(crochet_instructions_test4),"")

@route
def final_crochet_instructions(state:State)->Page:
    final = ""
    final = final_pattern_details(state) + "\n" + final_additional_details(state) + "\n" + final_instructions(state)
    return Page(state, [
        Header("Final Crochet Pattern"),
        final,
        Button("Back","index")])

final_instructions_test1 = State([CrochetInstructions(1,"6 sc in mr")], 0, SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(7,"Yarnsmiths","Chenille Chunky"))

final_instructions_test2 = State([CrochetInstructions(1,"6 sc in mr")], 0, SpecialInstructions(SafetyEyes(8,4,True),True),Pattern(0,"",""))

final_instructions_test3 = State([CrochetInstructions(1,"6 sc in mr")], 0, SpecialInstructions(SafetyEyes(8,4,True),True),Pattern(7,"Yarnsmiths","Chenille Chunky"))

final_instructions_test4 = State([], 0, SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))

#Row & Pattern Details
assert_equal(final_crochet_instructions(final_instructions_test1),
             Page(final_instructions_test1, [
                 Header("Final Crochet Pattern"),
                 "Hook Size: 7 mm \n Yarn Used: Yarnsmiths Chenille Chunky\nRow 1: 6 sc in mr\n",
                 Button("Back","index")
                 ]))
#Row & Special Instructions
assert_equal(final_crochet_instructions(final_instructions_test2),
             Page(final_instructions_test2, [
                 Header("Final Crochet Pattern"),
                 "Place 8mm Safety Eyes in Row 4\nStuff Project\nRow 1: 6 sc in mr\n",
                 Button("Back","index")
                 ]))

#Row, Special Instructions & Pattern details
assert_equal(final_crochet_instructions(final_instructions_test3),
             Page(final_instructions_test3, [
                 Header("Final Crochet Pattern"),
                 "Hook Size: 7 mm \n Yarn Used: Yarnsmiths Chenille Chunky\nPlace 8mm Safety Eyes in Row 4\nStuff Project\nRow 1: 6 sc in mr\n",
                 Button("Back","index")
                 ]))
#No inputs
assert_equal(final_crochet_instructions(final_instructions_test4),
             Page(final_instructions_test4, [
                 Header("Final Crochet Pattern"),
                 "",
                 Button("Back","index")
                 ]))

@route
def update_instructions(state:State)->Page:
    return Page(state, [
        Header("Update Row Instructions"),
        "Which Row would you like to update?",
        TextBox("row"),
        "Input updated instructions",
        TextBox("instructions"),
        Button("Save","save_update"),
        Button("Back","index")])

#initial update_instructions
assert_equal(update_instructions(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))),
    Page(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
    [
        Header("Update Row Instructions"),
        "Which Row would you like to update?",
        TextBox("row"),
        "Input updated instructions",
        TextBox("instructions"),
        Button("Save","save_update"),
        Button("Back","index")]))

@route
def save_update(state:State, row:int,instructions:str)->Page:
    for instruction in state.total_instructions:
        if row == instruction.row:
            instruction.complete_row_instructions = instructions
    return index(state)

#Update A Row
assert_equal(save_update(State([CrochetInstructions(1,"1 sc")],1,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),1,"6 sc"),
    Page(State([CrochetInstructions(1,"6 sc")],1,
            SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))

#Update Second Row
assert_equal(save_update(State([CrochetInstructions(1,"1 sc"),CrochetInstructions(2,"2 sc")],2,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),2,"1 inc"),
    Page(State([CrochetInstructions(1,"1 sc"),CrochetInstructions(2,"1 inc")],2,
            SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))


@route
def delete_instructions(state:State)->Page:
    return Page(state, [
        Header("Delete Row Instructions"),
        "Which Row Would You Like to Delete?",
        TextBox("row"),
        Button("Save","delete_row"),
        Button("Back","index")])

#initial delete instructions
assert_equal(delete_instructions(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"",""))),
    Page(State([],0,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
    [
        Header("Delete Row Instructions"),
        "Which Row Would You Like to Delete?",
        TextBox("row"),
        Button("Save","delete_row"),
        Button("Back","index")]))   

@route
def delete_row(state:State,row:int)->Page:
    remove_row = None
    for instructions in state.total_instructions:
        if instructions.row == row:
            remove_row = instructions
    if remove_row is not None:        
        state.total_instructions.remove(remove_row)
    state.current_row = state.current_row - 1     
    return index(state)
  
#delete one row 
assert_equal(delete_row(State([CrochetInstructions(1,"1 sc"),CrochetInstructions(2,"2 sc")],2,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),2),
    Page(State([CrochetInstructions(1,"1 sc")],1,
            SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))

#No more instructions
assert_equal(delete_row(State([CrochetInstructions(1,"1 sc")],1,SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),1),
    Page(State([],0,
            SpecialInstructions(SafetyEyes(0,0,False),False),Pattern(0,"","")),
                 [Header("Crochet Pattern Builder"),
                   "What would you like to do?",
                   Button("Add a Row", "stitch_instructions"),
                   Button("Update a Row", "update_instructions"),
                   Button("Delete a Row", "delete_instructions"),
                   Button("Insert Pattern Info", "pattern_info"),
                   Button("Insert Additional Instructions", "additional_instructions"),
                   Button("View Generated Instructions", "final_crochet_instructions")]))

start_server(State([],1,SpecialInstructions(SafetyEyes(0,0,False),False), Pattern(0,"","")))
