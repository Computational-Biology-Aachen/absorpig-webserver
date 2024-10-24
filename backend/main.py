import base64
import io

import matplotlib.pyplot as plt
import pandas as pd
from absorpig import routine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

origins = [
    "*",
    # "http://localhost",
    # "http://localhost:8000",
    # "http://localhost:5173",
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    absorption_spectrum: str
    chl_concentration: float
    mean_diameter: float
    pigment_spectrum: str | None
    shift_spectra: bool = True


class Result(BaseModel):
    pigment_composition: dict[str, float]
    img: str


def read_csv_from_str(s: str) -> pd.DataFrame:
    with io.StringIO(s) as fp:
        return pd.read_csv(fp, index_col=0)


@app.post("/")
async def root(
    ui: UserInput,
) -> Result:
    absorption_spectrum = read_csv_from_str(ui.absorption_spectrum).iloc[:, 0]

    if not ui.pigment_spectrum:
        print("Nope")
        pigment_spectrum = None
    else:
        pigment_spectrum = read_csv_from_str(ui.pigment_spectrum)

    results = routine(
        absorption_spectrum=absorption_spectrum,
        chl_concentration=ui.chl_concentration,
        mean_diameter=ui.mean_diameter,
        pigment_spectrum=pigment_spectrum,
        shift_spectra=ui.shift_spectra,
    )
    fig, _ = results.plot()

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format="png")
    plt.close(fig)
    img_bytes = base64.b64encode(img_buf.getvalue()).decode("utf-8")
    img_buf.close()

    return Result(
        pigment_composition=results.pigment_composition.to_dict(),
        img=img_bytes,
    )
