from pathlib import Path

import pylexibank
from clldutils.misc import slug


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "tjukabodyparts"

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"},
        separators="/",
        strip_inside_brackets=False,
    )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("Tjuka-2019.tsv", dicts=True, delimiter="\t")
        args.writer.add_sources((self.raw_dir / "source.bib").read_text(encoding="utf8"))


        concepts = args.writer.add_concepts(
            id_factory=lambda x: x.id.split("-")[-1] + "_" + slug(x.gloss),
            lookup_factory=lambda concept: concept.number,
        )

        languages = args.writer.add_languages()

        for row in data:
            for language in languages:
                args.writer.add_form(
                    Value=row[language],
                    Form=row[language],
                    Language_ID=language,
                    Parameter_ID=concepts[row["NUMBER"]],
                )