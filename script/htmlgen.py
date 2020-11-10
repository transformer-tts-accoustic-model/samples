r"""
    Generate Static HTML required to post on github
"""

from os import listdir,remove,path
import argparse

front_matter = r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Automaticaly generated content, please update scripts/htmlgen.py for any change -->
   <head>
      <meta charset="UTF-8">
      <title align="center">blah blah"</title>
      <style type="text/css">
        body, input, select, td, li, div, textarea, p {
        	font-size: 11px;
        	line-height: 16px;
        	font-family: verdana, arial, sans-serif;
        }

        body {
        	margin:5px;
        	background-color:white;
        }

        h1 {
        	font-size:16px;
        	font-weight:bold;
        }

        h2 {
        	font-size:14px;
        	font-weight:bold;
        }
      </style>
   </head>
   <body>
      <article>
         <header>
            <h1>Multi-rate attention architecture for fast streamable Text-to-speech spectrum modeling</h1>
         </header>
      </article>


      <div>
        <h2>Abstract</h2>
        <p>Typical high quality text-to-speech (TTS) systems today use a two-stage architecture, with a spectrum model stage that generates spectral frames and a vocoder stage that generates the actual audio. High-quality spectrum models usually incorporate the encoder-decoder architecture with self-attention or bi-directional long short-term (BLSTM) units. While these models can produce high quality speech, they often incur O(L) increase in both latency and real-time factor (RTF) with respect to input length L. In other words, longer inputs leads to longer delay and slower synthesis speed, limiting its use in real-time applications. In this paper, we propose a multi-rate attention architecture that breaks the latency and RTF bottlenecks by computing a compact representation during encoding and recurrently generating the attention vector in a streaming manner during decoding. The proposed architecture achieves high audio quality (MOS of 4.31 compared to groundtruth 4.48), low latency, and low RTF at the same time. Meanwhile, both latency and RTF of the proposed system stay constant regardless of input lengths, making it ideal for real-time applications.</p>
      </div>

      <h2> Supplementary audio samples </h2>
"""

back_matter = r"""
   </body>
</html>
"""


def get_row_column(root='./Long'):
    Columns = [x for x in listdir(root) if x[0] != '.']
    assert len(Columns) > 0, f"No subfolders under {root}/"
    Rows = set(listdir(f"{root}/{Columns[0]}"))
    for c in Columns:
        Rows = Rows.intersection(set(listdir(f"{root}/{c}")))

    cleanup(root,Rows,Columns)

    return list(Rows), Columns

def cleanup(root,rows,columns):
    for c in columns:
        for r in listdir(f"{root}/{c}"):
            if r not in rows:
                fpath = f"{root}/{c}/{r}"
                if args.delete:
                    assert path.isfile(fpath),f"{fpath} not single file"
                    remove(fpath)
                else:
                    print(f"would delete {fpath}")

def gen_table_header(name='noname', cols=["nothing"], file=None):
    print(f"""
    <div>
    <h2> {name} </h2>
      <table border = "1" class="inlineTable">
    """, file=file)
    print(
        ''.join([r"""
        <col width="300">""" for _ in cols]),
        file=file)
    print(
        """     <tr> """, file=file)
    print(
        ''.join([f"""
        <th>{col}</th>""" for col in cols]) +
        """
</tr>""", file=file)


def audio_entry(audio, file=None):
    print(
        f"""
    <td>
        <audio controls style="width: 200px;">
        <source src={audio} type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </td>""", file=file)


def text_entry(text, file=None):
    print(
        f"""
        <th>{text}</th>""",
        file=file)


def single_row(columns, text=True, file=None):
    print("<tr>", file=file)
    for c in columns:
        if(text):
            text_entry(c, file=file)
        else:
            audio_entry(c, file=file)
    print("</tr>", file=file)


def gen_table(args, file=None):
    for t in args.table:
        rows, cols = get_row_column(root=t)
        cols=['Groundtruth','Multi-rate','Multi-rate (no dynamic pooling)','LSTM','Self-attention','Tacotron2']
        gen_table_header(name=t, cols=cols, file=file)
        cols=['Groundtruth','Multi-rate','Multi-rate_no_pooling','LSTM','Self-attention','Tacotron2']
        for r in rows:
            c = [f"./{t}/{x}/{r}" for x in cols]
            single_row(c, text=args.name_only, file=file)
        print("""
            </table>
        </div>
        """, file=file)


def main(args):
    fname = args.output
    with open(fname, 'w') as f:
        print(front_matter, file=f)
        gen_table(args, file=f)
        print(back_matter, file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--output', type=str,
                        default='index.html', help='output name')
    parser.add_argument('-n', '--name_only',
                        action="store_true", help='put file names only')
    parser.add_argument('-t', '--table', type=str, action="append",
                        nargs='+', help='names of tables', default=['Normal', 'Long'])
    parser.add_argument('-del', '--delete',
                        action="store_true", help='delete files')


    global args
    args = parser.parse_args()

    main(args)
