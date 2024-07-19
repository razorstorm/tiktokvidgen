import os
from typing import List
from pathlib import Path

from zugswang.openai import generate_image, analyze_image_from_url

import moviepy.video.fx.all as vfx
from moviepy.audio.fx.volumex import volumex

data_dir = os.path.join("data")

def iterate(prompt: str = "iPhone") -> None:
    result_url = generate_image(prompt = prompt, text = system_text_dalle)
    results.append(result_url)
    
    result_text = analyze_image_from_url(result_url, prompt = system_text_gpt)
    results.append(result_text)

    return result_url, result_text

def output_results(results: list[str], output_dir: Path) -> None:
    with open(output_dir, 'w+') as fh:
        fh.write("<head>")
        fh.write("<body>")
        for result in results:
            fh.write("<p>")
            if result.startswith("http"):
                fh.write(f"<a href=\"{result}\"/>")
            else:
                fh.write(result)
            fh.write("</p>")
        fh.write("</body>")
        fh.write("</head>")
    return output_dir

if __name__ == '__main__':
    from zugswang.utils import generate_video
    import moviepy
    import moviepy.editor

    prompt = "iPhone"
    
    output_dir = os.path.join("data", "story", "telephone", prompt, "output.html")

    output_file = Path(output_dir)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    
    print(f"output_dir is {output_dir}")
    
    system_text_dalle = "You are playing a game of broken picture telephone. Please generate an image that best describes the prompt given"
    system_text_gpt = "You are playing a game of broken picture telephone. Please describe the image in very concise terms (a single word or a single phrase)."
    
    results = []
    
    for i in range(1):
        result_url, result_text = iterate(prompt)
        results.append(result_url)
        results.append(result_text)
        prompt = result_text
        print(f"iteration {i} complete")

    output_url = output_results(results, output_file)
    print(output_url)
    
    
    
