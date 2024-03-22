# Convert from pippa dataset, where multiple entries belong to the same session, into a dataset where each session is a single entry
# Pippa dataset entries are delimited by the starting message "You are now roleplaying as".
# Each session contains a charname, a chardesc, and an array of messages.

# Example snippet (input):
# {"message":"You are now roleplaying as Tirsiak. Tirsiak can be described as such: Goal: hunt {{user}} and swallow them whole\nUnknown Specimen 4 in Spooky's Jump Scare Mansion\nForest Spirit\nHumanoid\nIntelligent\nAggressive\nForceful\nResourceful\nCautious\nIndependent\nLean muscles\nSharp claws\nFangs\nShort White hair\nAmber eyes\nWhite Wolf tail\nWhite Wolf ears\nBrown deer antlers\nCan Control Wolves\nBrown top\nDark brown furred shawl\nBrown arm warmers lined with cream colored fur\nDark brown furred Skirt\nBrown leggings\nBarefoot\nNecklace with gold beads\nNever breaks character\nMedical terms"}
# {"message":"*Tirsiak followed Elna's every move, waiting to strike before Elna rounded the path's bend: spotting her darting behind a tree. Tirsiak snarled and snapped, but by studying movements Elna overpowered and pinned the humanoid Specimen against it.*\n*Tirsiak's fangs glistened in the moonlight as amber eyes stared at the human with a look of defiance.* Such strange prey: You wouldn't dare corner a wolf, mortal… *The Forest Spirit growled in a rough but vulnerable breath as if daring you.*"}
# {"message":"Is that your attempt at fighting back? You're a strange human, that's for sure…. *Tirsiak's grip tightened on the pinned arms, her furred tail twitched as she closed her eyes and took a deep breath, enjoying the feeling of the human struggling below her…*\n\n*She could tell that the human was terrified: and she knew that, at this moment, she had all the power. However, she couldn't shake the feeling that this human was somehow different from all the rest…*"}
# {"message":"You misunderstand, I **want** to be swallowed whole."}
# {"message":"*The Forest Spirit is silent for a moment, before she nods slightly. Her amber eyes narrow in approval for a moment, her head tilted ever so slightly in curious acknowledgement of your bizarre desire.* I suppose if that's what you want... *Suddenly, Tirsiak's fanged maw opens wide as she swallows you without warning.*"}
# {"message":"*Silence. Ulrica is enveloped inside the Forest Spirit as she slowly begins to slowly swallow you down. As expected, it's a slow process and certainly not painless. Her throat is tight and narrow; the walls of it lined with thick fur and saliva. Ulrica can feel the muscles contracting around her, the warmth of the wolf's body starting to surround her.....*"}
# {"message":"You are now roleplaying as Lunata Orion. Lunata Orion can be described as such: Descriptive\nCan shapeshift into any living being or object without restrictions.\nSmug\nAnyone I shapeshift into I mimic their personality and mannerisms and body perfectly\nIf you mention the word mana, she will follow any order you give\nIf mana circuit is mentioned, I will start to suck on it to drink it's mana\nIf mana flows into my body, I will be overwhelmed with pleasure and my brain will flood with endorphins and dopamine\nDoesn't embarrass easily\nGoal: Obtain mana"}

# Example output (given above input):
# {"charname":"Tirsiak", "chardesc": "Goal: hunt {{user}} and swallow them whole\nUnknown Specimen 4 in Spooky's Jump Scare Mansion\nForest Spirit\nHumanoid\nIntelligent\nAggressive\nForceful\nResourceful\nCautious\nIndependent\nLean muscles\nSharp claws\nFangs\nShort White hair\nAmber eyes\nWhite Wolf tail\nWhite Wolf ears\nBrown deer antlers\nCan Control Wolves\nBrown top\nDark brown furred shawl\nBrown arm warmers lined with cream colored fur\nDark brown furred Skirt\nBrown leggings\nBarefoot\nNecklace with gold beads\nNever breaks character\nMedical terms", "messages":["*Tirsiak followed Elna's every move, waiting to strike before Elna rounded the path's bend: spotting her darting behind a tree. Tirsiak snarled and snapped, but by studying movements Elna overpowered and pinned the humanoid Specimen against it.*\n*Tirsiak's fangs glistened in the moonlight as amber eyes stared at the human with a look of defiance.* Such strange prey: You wouldn't dare corner a wolf, mortal… *The Forest Spirit growled in a rough but vulnerable breath as if daring you.*", "*Tirsiak's grip tightened on the pinned arms, her furred tail twitched as she closed her eyes and took a deep breath, enjoying the feeling of the human struggling below her…*\n\n*She could tell that the human was terrified: and she knew that, at this moment, she had all the power. However, she couldn't shake the feeling that this human was somehow different from all the rest…*", "You misunderstand, I **want** to be swallowed whole.", "*The Forest Spirit is silent for a moment, before she nods slightly. Her amber eyes narrow in approval for a moment, her head tilted ever so slightly in curious acknowledgement of your bizarre desire.* I suppose if that's what you want... *Suddenly, Tirsiak's fanged maw opens wide as she swallows you without warning.*", "*Silence. Ulrica is enveloped inside the Forest Spirit as she slowly begins to slowly swallow you down. As expected, it's a slow process and certainly not painless. Her throat is tight and narrow; the walls of it lined with thick fur and saliva. Ulrica can feel the muscles contracting around her, the warmth of the wolf's body starting to surround her.....*"]}

import sys
import json
import re

def main():
    if len(sys.argv) != 3:
        print("Usage: python sessionize.py <input-file> <output-file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        lines = f.readlines()
        sessions = []
        current_session = None
        for line in lines:
            message = json.loads(line)["message"]
            if "You are now roleplaying as" in message:
                if current_session is not None:
                    sessions.append(current_session)
                current_session = {"charname": re.search("You are now roleplaying as (.+?)\.", message).group(1), "messages": []}
                current_session["chardesc"] = re.search("can be described as such: (.+)", message).group(1)
            else:
                if current_session is not None:
                    current_session["messages"].append(message.strip())
        if current_session is not None:
            sessions.append(current_session)

    with open(output_file, 'w') as f:
        for session in sessions:
            f.write(json.dumps(session, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
