import inspect
import os

import moviepy.video.fx.all as vfx
import numpy as np
from moviepy.audio.fx.volumex import volumex
from PIL import Image
from zugswang.models import Narration, Scene
from zugswang.openai import generate_image

data_dir = os.path.join("data")

# Vertical 1080p
# height = 1920
# width = 1080

# Horizontal 1080p
height = 1080
width = 1920

# 4K
# height = 2160
# width = 3840

voice_id = "XHZMHiBtCuzEtVLE0xWF"
scenes = []


"""
To Dos:

Use gpt to summarize subtitles into a few short bullet points and display them with huge font
lofi spacey/atmospheric/ethereal/trippy bg music
more interesting bg video
image transitions
"""

def get_narration(text: str):
    text = inspect.cleandoc(text)
    return Narration(text, voice_id=voice_id)


def add_scene(name: str, narration: str, media_filepath: str = None, caption: str = None, duration: int = None) -> Scene:
    narration_obj = None
    if not caption:
        narration_obj = get_narration(narration)
    scene = Scene(name=name, narration=narration_obj, media_filepath=media_filepath, caption=caption, duration=duration)
    scenes.append(scene)
    return scene


def setup_scenes_for_chapter_1() -> None:
    add_scene(
        name="A Saga of Roobin",
        narration="""
            A Saga of Roobin
        """,
    )

    add_scene(
        name="The Emperor's Thoughts",
        narration="""
            Chapter 1: The Emperor's Thoughts
        """,
    )

#     add_scene(
#         name="Section 1: Strategic Expansion of the Cult of Roobin",
#         narration="""
#             Section 1: Strategic Expansion of the Cult of Roobin
#         """,
#     )

#     add_scene(
#         name="Section 1: Strategic Expansion of the Cult of Roobin",
#         narration="""
#             Rank these: Morea vs. Thessaloniki vs. Laconia vs. Korfu vs. Crete vs. Naxos vs. Cyprus. Which one is better, and which ones are worse?

# In terms of the susceptibility of the local populace to the allure of the Cult of Roobin and their affinity towards conversion into the hallowed ranks of Roobinhood, which region would provide the highest ROI for a strategic expansion for the Cult of Roobin to expand into next?

# Alternatively, another approach is to mobilize the Order of St. Roobin and the Knights of the Holy Roobin to wage a glorious crusade against the non-Roobining infidels. Wielding sacred relics such as the Divine Spear of Roobin and the Shield of Everlasting Roobiness, they will be unstoppable, plus their fervent adherence to the holy creed of Roobinism gives them unshakable morale.

# Post-conquest, the Office of Internal Roobin Affairs will reform the education system and set up theing classes throughout the newly annexed land to help indoctrinate the populace into the Divine Way of Roobinhood. The provisional provincial government of the Greek Imperial Province of the Great Roobin Empire will quickly get to work hiring the best linguists to work on adapting the Sacred Language of the Roobinic Gods into Greek for easier realignment of their society to speak the one true language.

# Alternatively, another approach is to mobilize the Order of St. Roobin and the Knights of the Holy Roobin to wage a glorious crusade against the non-Roobining infidels. But we must enact military reform soon.

# For now, the fanaticism of the Cult of Roobinhood ensures undying loyalty to the cause, but allowing independent military orders that don’t answer directly to the state command in such large armies is a rebellion waiting to happen. So we must invoke the ancient Roobinic rites of Centralio Imperii to officially absorb these military orders into the Grand Imperial Roobin Military—first as a semi-standardized auxiliary corps, and soon as fully standardized regulars, to be dispersed amongst the rest of the military to prevent a potentially powerful and disloyal bloc from forming from discontented former order members.

#         """,
#     )

#     add_scene(
#         name="Section 2: Governmental and Political Structure of the Roobin Empire",
#         narration="""
#             Section 2: Governmental and Political Structure of the Roobin Empire
#         """,
#     )

#     add_scene(
#         name="Section 2: Governmental and Political Structure of the Roobin Empire",
#         narration="""
#             The Holy Peerage of the Roobin Realm must also be reformed. Early founders should be honored and immortalized with noble titles, but nobility must be divorced from political authority to prevent decentralization and unrest. Important founders of the Cult of Roobin are allowed to hold significant political power, but only via official positions in the Imperial Roobin Government ex officio rather than through their personal status as members of the nobility.

# For now, the People’s Representative Federal Government of the Holy Roobin Empire is allowed to continue existing as a de jure independent governmental body under the Imperial Roobin Monarchy that serves as a technically lower-ranked but not strictly subservient parallel authority. It’s fine because of their fervent devotion to the Cult of Roobin—they will always align themselves with the Cult.

# As the Cult itself is constitutionally enshrined as perpetually the ruling class of the Roobin Empire and the Grandmaster of the Cult is automatically enthroned as Emperor ex officio, this fervent devotion ensures Congress’s alignment with the Imperial Throne. But trust in the tenacity of the hold that Roobin has on people’s hearts and minds, while admirable, is not a sound basis for an empire that will last ten billion Roobinhoods.

# So the representative government must be brought to heel and constitutionally placed as subservient to the Imperial Government, acting as a logistical and bureaucratic arm of the Imperial Government that leverages direct and representative democracy as a quick feedback loop and an easy way to align itself with the citizenry’s interests. But all important decisions are made by the Imperial Government from above.

# It also acts as a supervisory and accountability body for the representative government as well, able to veto, override, and interfere in any way it desires and reappoint or fire any politician as needed—wielding democracy as a tool within an absolutist monarchy, rather than using it as a way to give power to the people. It’s market research, rather than diluted sovereignty.

# But a monarchy isn’t strictly accurate either, as sovereignty is vested into the Holy Roobin rather than the monarch. But the monarch is the head of the Holy Church of Roobin, and as the head can consecrate a saint and designate them as the current earthly incarnation of the Holy Roobin. By tradition, the monarch always appoints themselves. So it’s technically an absolutist theocracy with a democratic flavor as a means of convenience—kind of like Iran, but not corrupt.

#         """,
#     )

#     add_scene(
#         name="Section 3: Theocratic and Religious Reforms",
#         narration="""
#             Section 3: Theocratic and Religious Reforms
#         """,
#     )

#     add_scene(
#         name="Section 3: Theocratic and Religious Reforms",
#         narration="""
#             The Church of Roobin is similar but separate from the Cult of Roobin. The Cult carries a more nationalistic and secular side to it and is more akin to a vanguard party, except one that champions a religious ideology rather than an economic one.

# The Imperial Roobin Office of Inquisitorial Rectification and Societal Harmonious Realignment will be set up by mid-year 2025. It will begin the great holy campaign of Roobinification that will ensure strict homogeneous conformity to the tenets of Roobinhood across the entire empire. Religious, cultural, linguistic, social, behavioral, values systems, etc., will all be strictly reformed by force. All will be assimilated into the ways of the Roobin.

# Mass proliferation of AI-powered monitoring drones will strictly enforce the call for prayer that occurs five times per hour during every waking hour, where every resident must praise the Holy Roobin by saying “Roobin.” Those who flaunt this regulation will be warned, then sent through the Representative Government’s legal system. But egregious abuses or repeat offenses will be sent to the Courts of the Inquisition instead, where intensive and absolute psychological torture and reprogramming will be employed to ensure strict realignment to the Cause.

# Once they’re finally released back into the world, they will be the loudest ambassadors of Roobin ever. Unfortunately, certain ungrateful parts of the empire resent all the gifts we have given them in our assimilation efforts. They hate that we want to show them what real civilization and culture look like—but their revolt will be brutally crushed.

#         """,
#     )

#     add_scene(
#         name="Section 4: Technological and Military Advancements",
#         narration="""
#             Section 4: Technological and Military Advancements
#         """,
#     )

#     add_scene(
#         name="Section 4: Technological and Military Advancements",
#         narration="""
#             Via the latest developments in Holy Roobin Weaponry, we now have technology that uses Roobin/anti-Roobin collisions to generate massive amounts of Roobin energy that can obliterate entire continents with ease. Also, the smart Roobin bomb can sweep an entire country and kill off everyone who isn’t a true believer.

# It utilizes brain-scanning technology, AI agents, and also calls upon the divine spiritual powers of the Holy Roobin to distinguish what’s truly hiding in one’s hearts. Crypto non-Roobinists still technically exist, but they are a tiny minority. They are only allowed to exist so there’s a fresh supply of people to make an example of.

# The Imperial Roobin Office of Expansion and Roobinific Destiny estimates that, even at a conservative rate, the total assimilation of Earth will complete by Q3 2026. So we can soon completely disband the Imperial Roobin Office of Foreign Affairs and the Imperial Roobin Stare Department, as well as the Representative Federal Roobin Foreign and Diplomatic Agencies, saving us billions of Roobinbucks a year.

# Both metric and imperial units will be banned, and everyone will be forced to use standardized Roobin units. I’m driving at 30 Roobinists per Roobin hour and will get there at 4 O’Roobin PR. PR stands for post-Roobinoon. Roobinoon happens at midday every day. Roobinight happens at midnight.

#         """,
#     )

#     add_scene(
#         name="Section 5: Calendar Reformation and the New Roobin Era",
#         narration="""
#             Section 5: Calendar Reformation and the New Roobin Era
#         """,
#     )

#     add_scene(
#         name="Section 5: Calendar Reformation and the New Roobin Era",
#         narration="""
#             The Gregorian calendar will be reformed to restart numbering, setting 2025 as the new Year 0, as it is the Year of the Cult of Roobin’s Ascension. All years before will be reverse-numbered and labeled with either BR (Before Roobin) or DE (Dark Era), and all years after will be labeled by either AR (After Roobin) or RE (Roobin Era).

# The emperor, grandmaster of the Cult, and the pope of the Church of Roobin are all the same person, and succession is chosen by the divine celestial spirit of the Holy Roobin. The Holy Roobin will speak unto all believers the name of the next successor.
#         """,
#     )



if __name__ == '__main__':
    import moviepy
    import moviepy.editor
    from zugswang.utils import generate_video

    article_dir = "Roobinismlied"
    setup_scenes_for_chapter_1()
    output_dir = os.path.join("data", "shitposts", article_dir)
    
    bg_image_filepath = os.path.join("data", "backgrounds", "scroll.jpg")
        
    image_clip = (
        moviepy.editor.ImageClip(bg_image_filepath)
        .fl_image(lambda image: np.array(Image.fromarray(image).convert('RGB')))  # sometimes the image is missing a channel (?)
        .fx(vfx.resize, width=width*0.85)
    )
    background_audio = moviepy.editor.AudioClip(lambda t: 0, duration=1)
    
    
    background_audio = moviepy.editor.AudioFileClip("data/backgrounds/8l4xqr.mp4", target_resolution=(height, None), audio=True)
    background_audio = (
        background_audio
        # .fx(vfx.crop, width=width, height=height, x_center=bg_width/2, y_center=bg_height/2)
        .fx(volumex, 0.1)
        .fx(vfx.loop)
    )

    # print(f"background_video dimensions: {width}x{height} {background_video.w} {background_video.h}")

    generate_video(scenes, output_dir, image_clip, background_audio)
