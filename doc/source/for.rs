#![feature(default_free_fn)]

use itertools::{izip, Itertools};
use maplit::hashmap;
use std::{default::default, iter::Sum};

// fn temp(iter: impl Iterator<Item = (f32, f32)>) -> impl Iterator<Item = f32> {
//     iter.map(|(i, item)| item / 10.0 * wag[i])
// }

// let l = |s: f64| s / 10.0 * m;

// let sum = |s: &[f32]| -> f32 {
//     let mut sum = 0.0;
//     for i in 0..len {
//         sum += s[i] / 10.0 * wag[i];
//     }
//     sum
// };

// let relative = |s| -> Vec<f32> {
//     let sum = sum(s);
//     s.iter().map(|s| s / sum).collect()
// };

// Если убрать 10.0, то значения 1,2-DAGs и 1,2,3-TAGs изменятся, а значения
// 1,3-TAGs и 2-TAGs останутся неизменными.
fn dm<'a>(s: &'a [f64], m: &'a [f64]) -> impl Iterator<Item = f64> + 'a {
    izip!(s, m).map(|(s, m)| s * m / 10.0)
}

struct Pair {
    relative: Vec<f64>,
    absolute: Vec<f64>,
}

impl Pair {
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            absolute: Vec::with_capacity(capacity),
            relative: Vec::with_capacity(capacity),
        }
    }
}

fn main() {
    let efirs = &["Pi", "Pa", "Pn", "Gd", "St", "Ol", "Ar", "Li", "Ln"];
    // Molecular weight
    let m = &[
        294.462, 270.442, 292.446, 322.414, 298.494, 296.478, 326.546, 294.462, 292.446,
    ];

    let s = &[
        (18, 2),
        (16, 0),
        (18, 3),
        (20, 1),
        (18, 0),
        (18, 1),
        (20, 0),
        (18, 2),
        (18, 3),
    ];

    // Peak Area Total TAGs
    // let b = &[
    //     0042194.0, 0145011.0, 0599666.0, 0025799.0, 0074037.0, 0595393.0, 0007738.0, 1158289.0,
    //     0005070.0,
    // ];
    let tags123 = vec![
        42194071.111,
        145011164.005,
        599666360.160,
        25798972.603,
        74037315.870,
        595392558.250,
        7737659.800,
        1158289211.401,
        5070004.063,
    ];
    // Peak Area Free 1,2-DAGs
    // 208042.0, 302117.0, 2420978.0, 85359.0, 195625.0, 2545783.0, 31482.0, 4819586.0, 12823.0,
    let dags12 = vec![
        208041598.375,
        302116780.058,
        2420977752.198,
        85358549.162,
        195624715.683,
        2545783364.126,
        31481582.538,
        4819585526.736,
        12823290.138,
    ];

    let mut mim = [[0.0; 9]; 9];

    let len = efirs.len();
    assert_eq!(len, tags123.len());
    assert_eq!(len, dags12.len());
    assert_eq!(len, m.len());

    // 1,2,3-TAGs
    let sum: f64 = dm(&tags123, m).sum();
    println!("sum: {sum}");
    let tags123 = Pair {
        relative: tags123.iter().map(|s| s / sum).collect(),
        absolute: tags123,
    };
    println!(
        "tags123.relative: {:?}",
        tags123.relative.iter().sum::<f64>()
    );

    // 1,2-DAGs
    let sum: f64 = dm(&dags12, m).sum();
    let dags12 = Pair {
        relative: dags12.iter().map(|s| s / sum).collect(),
        absolute: dags12,
    };

    // 2-TAGs
    // Формула у пчелкина
    let mec: Vec<_> = (0..len)
        .map(|i| 0.0f64.max(4.0 * dags12.relative[i] - 3.0 * tags123.relative[i]))
        .collect();
    println!("mec: {:?}", mec);
    let sum: f64 = mec.iter().sum();
    let mut tags2 = Pair::with_capacity(len);
    for i in 0..len {
        let relative = mec[i] / sum;
        tags2.relative.push(relative);
        tags2.absolute.push(relative / tags123.relative[i])
    }
    println!("tags2.relative: {:?}", tags2.relative.iter().sum::<f64>());

    // 1,3-TAGs (sn2?)
    // Формула у Ромы
    let mut sum = 0.0;
    let mut med = Vec::with_capacity(len);
    for i in 0..len {
        med.push((3.0 * tags123.relative[i] - 2.0 * dags12.relative[i]).max(0.0));
        sum += med[i];
    }
    let mut tags13 = Pair::with_capacity(len);
    for i in 0..len {
        let relative = med[i] / sum;
        tags13.relative.push(relative);
        tags13.absolute.push(relative / tags123.relative[i])
    }
    println!("tags13.relative: {:?}", tags13.relative.iter().sum::<f64>());

    // let temp = |f: Fn() -> f32| {
    //     let mut sum = 0.0;
    //     let mut med = Vec::with_capacity(len);
    //     for i in 0..len {
    //         med.push((3.0 * tags123.relative[i] - 2.0 * dags12.relative[i]).max(0.0));
    //         sum += med[i];
    //     }
    //     let mut tags13 = Pair::with_capacity(len);
    //     for i in 0..len {
    //         let relative = med[i] / sum;
    //         tags13.relative.push(relative);
    //         tags13.absolute.push(relative / tags123.relative[i])
    //     }
    //     tags13
    // };

    // for i in 0..9 {
    //     for j in 0..9 {
    //         mim[i][j] = mdl[i] * mdl[j];
    //     }
    // }

    println!("Sample_TAG_of_seed_Pinus_oil_Year_2023_Stage_III\n");
    println!("Date:_23-05-2023_Mole_Part_TOTAL_REPORT_AGILENT\n");

    println!("N |  GLC Peak Area | Free 1,2-DAGs");
    for i in 0..9 {
        println!(
            "{i}   {:>14.3}   {:.5}",
            dags12.absolute[i], dags12.relative[i]
        );
    }

    println!("\nN |  GLC Peak Area | 1,2,3-TAGs");
    for i in 0..9 {
        println!(
            "{i}   {:>14.3}   {:.5}",
            tags123.absolute[i], tags123.relative[i]
        );
    }

    println!("\nN |    Selectivity | 2-TAGs");
    for i in 0..9 {
        println!(
            "{i}   {:>14.3}   {:.5}",
            tags2.absolute[i], tags2.relative[i]
        );
    }

    println!("\nN |    Selectivity | 1,3-TAGs");
    for i in 0..9 {
        println!(
            "{i}   {:>14.3}   {:.5}",
            tags13.absolute[i], tags13.relative[i]
        );
    }

    println!("\nCALCULATED_TAG_COMPOSITION");
    println!("__N_TAG_species_Mole_Parts");
    let mut k = 0;
    for i in 0..9 {
        for j in 0..9 {
            k = k + 1;
            let bm = mim[i][j] * tags2.relative[2];
            if bm >= 0.001 {
                println!("{:03} Pi{}{}        {:7.5}", k, efirs[i], efirs[j], bm);
            }
        }
    }
    let mut im = 0.0;
    for i in 0..9 {
        for j in 0..9 {
            let bm = mim[i][j] * tags2.relative[2];
            if bm < 0.001 {
                im = im + bm;
            }
        }
    }
    k = 81;
    for i in 0..9 {
        for j in 0..9 {
            k = k + 1;
            let cm = mim[i][j] * tags2.relative[3];
            if cm >= 0.001 {
                println!("{:03} Pa{}{}       {:7.5}", k, efirs[i], efirs[j], cm);
            }
        }
    }
    for i in 0..9 {
        for j in 0..9 {
            let cm = mim[i][j] * tags2.relative[3];
            if cm < 0.001 {
                im = im + cm;
            }
        }
    }
    k = 162;
    for i in 0..9 {
        for j in 0..9 {
            k = k + 1;
            let dm = mim[i][j] * tags2.relative[6];
            if dm >= 0.001 {
                println!("{:03} Pn{}{}       {:7.5}", k, efirs[i], efirs[j], dm);
            }
        }
    }
    for i in 0..9 {
        for j in 0..9 {
            let dm = mim[i][j] * tags2.relative[6];
            if dm < 0.001 {
                im = im + dm;
            }
        }
    }
    k = 243;
    for i in 0..9 {
        for j in 0..9 {
            k = k + 1;
            let em = mim[i][j] * tags2.relative[7];
            if em >= 0.001 {
                println!("{:03} Gd{}{}        {:7.5}", k, efirs[i], efirs[j], em);
            }
        }
    }
    for i in 0..9 {
        for j in 0..9 {
            let em = mim[i][j] * tags2.relative[7];
            if em < 0.001 {
                im = im + em;
            }
        }
    }
    k = 324;
    for i in 0..9 {
        for j in 0..9 {
            k = k + 1;
            let fm = mim[i][j] * tags2.relative[8];
            if fm >= 0.001 {
                println!("{:03} St{}{}       {:7.5}", k, efirs[i], efirs[j], fm);
            }
        }
    }
    for i in 0..9 {
        for j in 0..9 {
            let fm = mim[i][j] * tags2.relative[8];
            if fm < 0.001 {
                im = im + fm;
            }
        }
    }
    // k = 405;
    // for i in 0..9 {
    //     for j in 0..9 {
    //         k = k + 1;
    //         let gm = mim
}
