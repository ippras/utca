fn main() {
    let mut wag: [f64; 9] = [0.0; 9];
    let mut a: [f64; 9] = [0.0; 9];
    let mut b: [f64; 9] = [0.0; 9];
    let mut c: [f64; 9] = [0.0; 9];
    let mut d: [f64; 9] = [0.0; 9];
    let mut m: [f64; 9] = [0.0; 9];
    let mut mal: [f64; 9] = [0.0; 9];
    let mut mbl: [f64; 9] = [0.0; 9];
    let mut mcl: [f64; 9] = [0.0; 9];
    let mut mdl: [f64; 9] = [0.0; 9];
    let mut mec: [f64; 9] = [0.0; 9];
    let mut med: [f64; 9] = [0.0; 9];
    let mut mim: [[f64; 9]; 9] = [[0.0; 9]; 9];
    let mut imi: f64 = 0.0;
    let mut imk: f64 = 0.0;
    let efir: [char; 9] = ['\0'; 9];

    wag[0] = 294.462;
    wag[1] = 270.442;
    wag[2] = 292.446;
    wag[3] = 322.414;
    wag[4] = 298.494;
    wag[5] = 296.478;
    wag[6] = 326.546;
    wag[7] = 294.462;
    wag[8] = 292.446;

    efir[0] = 'P';
    efir[1] = 'i';
    efir[2] = 'P';
    efir[3] = 'a';
    efir[4] = 'P';
    efir[5] = 'n';
    efir[6] = 'G';
    efir[7] = 'd';
    efir[8] = 'S';

    a[0] = 208042.0;
    a[1] = 302117.0;
    a[2] = 2420978.0;
    a[3] = 85359.0;
    a[4] = 195625.0;
    a[5] = 2545783.0;
    a[6] = 31482.0;
    a[7] = 4819586.0;
    a[8] = 12823.0;

    b[0] = 42194.0;
    b[1] = 145011.0;
    b[2] = 599666.0;
    b[3] = 25799.0;
    b[4] = 74037.0;
    b[5] = 595393.0;
    b[6] = 7738.0;
    b[7] = 1158289.0;
    b[8] = 5070.0;

    let mut sam: f64 = 0.0;
    for i in 0..9 {
        sam += a[i] / 10.0 * wag[i];
    }

    for i in 0..9 {
        mal[i] = a[i] / sam;
    }

    let mut sbm: f64 = 0.0;
    for i in 0..9 {
        sbm += b[i] / 10.0 * wag[i];
    }

    for i in 0..9 {
        mbl[i] = b[i] / sbm;
    }

    for i in 0..9 {
        mec[i] = 4.0 * mal[i] - 3.0 * mbl[i];
        if mec[i] < 0.0 {
            mec[i] = 0.0;
        }
    }

    let mut scm: f64 = 0.0;
    for i in 0..9 {
        scm += mec[i];
    }

    for i in 0..9 {
        mcl[i] = mec[i] / scm;
    }

    for i in 0..9 {
        med[i] = 3.0 * mbl[i] - 2.0 * mal[i];
        if med[i] < 0.0 {
            med[i] = 0.0;
        }
    }

    let mut sdm: f64 = 0.0;
    for i in 0..9 {
        sdm += med[i];
    }

    for i in 0..9 {
        mdl[i] = med[i] / sdm;
    }

    for i in 0..9 {
        for j in 0..9 {
            mim[i][j] = mdl[i] * mdl[j];
        }
    }

    for i in 0..9 {
        c[i] = mcl[i] / mbl[i];
    }

    for i in 0..9 {
        d[i] = mdl[i] / mbl[i];
    }

    // tags123:
    // - b - raw
    // - mbl - unnormalized
    // - sbm - sum
    //
    // dags1223:
    // - a - raw
    // - mal - unnormalized
    // - sam - sum
    //
    // mags2:
    // - c - raw (selectivity) `mcl / mbl`
    // - mec - unnormalized
    // - mcl - normalized
    // - scm - sum
    //
    // dags13:
    // - d - raw (selectivity) `mdl / mbl`
    // - med - unnormalized
    // - mdl - normalized
    // - sdm - sum
    println!("Sample_TAG_of_seed_Pinus_oil_Year_2023_Stage_III");
    println!("Date:_23-05-2023_Mole_Part_TOTAL_REPORT_AGILENT");
    println!("_N___GLC_Peak_Area__Free_1,2-DAGs");
    for i in 0..9 {
        println!("{:2} {:15.0} {:7.5}", i + 1, a[i], mal[i]);
    }

    println!("_N___GLC_Peak_Area__Total_TAGs");
    for i in 0..9 {
        println!("{:2} {:15.0} {:7.5}", i + 1, b[i], mbl[i]);
    }

    println!("_N_______Selectivity___________2-TAGs");
    for i in 0..9 {
        println!("{:2}    {:15.0}     {:7.5}", i + 1, c[i], mcl[i]);
    }

    println!("_N_______Selectivity_________1,3-TAGs");
    for i in 0..9 {
        println!("{:2}    {:15.0}     {:7.5}", i + 1, d[i], mdl[i]);
    }

    println!("CALCULATED_TAG_COMPOSITION");
    println!("__N_TAG_species_Mole_Parts");
    let mut k = 0;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let bm = mim[i][j] * mcl[1];
            if bm >= 0.001 {
                println!("{:3} Pi{}{}{:7.5}", k, efir[i], efir[j], bm);
            }
        }
    }

    let mut im = 0.0;
    for i in 0..9 {
        for j in 0..9 {
            let bm = mim[i][j] * mcl[1];
            if bm < 0.001 {
                imi = im + bm;
            }
        }
    }

    k = 81;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let cm = mim[i][j] * mcl[2];
            if cm >= 0.001 {
                println!("{:3} Pa{}{}{:7.5}", k, efir[i], efir[j], cm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let cm = mim[i][j] * mcl[2];
            if cm < 0.001 {
                imi = imi + cm;
            }
        }
    }

    k = 162;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let dm = mim[i][j] * mcl[5];
            if dm >= 0.001 {
                println!("{:3} Pn{}{}{:7.5}", k, efir[i], efir[j], dm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let dm = mim[i][j] * mcl[5];
            if dm < 0.001 {
                imi = imi + dm;
            }
        }
    }

    k = 243;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let em = mim[i][j] * mcl[6];
            if em >= 0.001 {
                println!("{:3} Gd{}{}{:7.5}", k, efir[i], efir[j], em);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let em = mim[i][j] * mcl[6];
            if em < 0.001 {
                imi = imi + em;
            }
        }
    }

    k = 324;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let fm = mim[i][j] * mcl[7];
            if fm >= 0.001 {
                println!("{:3} St{}{}{:7.5}", k, efir[i], efir[j], fm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let fm = mim[i][j] * mcl[7];
            if fm < 0.001 {
                imi = imi + fm;
            }
        }
    }

    k = 405;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let gm = mim[i][j] * mcl[3];
            if gm >= 0.001 {
                println!("{:3} Ol{}{}{:7.5}", k, efir[i], efir[j], gm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let gm = mim[i][j] * mcl[3];
            if gm < 0.001 {
                imi = imi + gm;
            }
        }
    }

    k = 486;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let hm = mim[i][j] * mcl[4];
            if hm >= 0.001 {
                println!("{:3} Ar{}{}{:7.5}", k, efir[i], efir[j], hm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let hm = mim[i][j] * mcl[4];
            if hm < 0.001 {
                imi = imi + hm;
            }
        }
    }

    k = 567;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let jm = mim[i][j] * mcl[0];
            if jm >= 0.001 {
                println!("{:3} Li{}{}{:7.5}", k, efir[i], efir[j], jm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let jm = mim[i][j] * mcl[0];
            if jm < 0.001 {
                imi = imi + jm;
            }
        }
    }

    k = 648;
    for i in 0..9 {
        for j in 0..9 {
            k += 1;
            let lm = mim[i][j] * mcl[8];
            if lm >= 0.001 {
                println!("{:3} Ln{}{}{:7.5}", k, efir[i], efir[j], lm);
            }
        }
    }

    for i in 0..9 {
        for j in 0..9 {
            let lm = mim[i][j] * mcl[8];
            if lm < 0.001 {
                imi = imi + lm;
            }
        }
    }

    println!("Total_Minor_species");
    println!("{:19}", imi);
    println!("Calculated_S2_Value,_Mole_Parts");
    imk = 2.0 * mcl[0] + 3.0 * mcl[2] + mcl[3] + mcl[6] + 2.0 * mcl[7] + 3.0 * mcl[8];
    println!("{:19}", imk);
}
