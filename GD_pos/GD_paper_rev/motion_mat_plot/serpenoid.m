function joint_pos = serpenoid(t, b, b2, a, a2, e_d1, e_d2, e_l1, e_l2, delta)

    f1 = e_d2 * t;
    f2 = e_l2 * t;

    j_1 = b + a * sin(e_d1 + f1);
    j_2 = b2 + a2 * sin(e_l1 * 2 + f2 + delta);

    j_3 = b + a * sin(e_d1 * 3 + f1);
    j_4 = b2 + a2 * sin(e_l1 * 4 + f2 + delta);

    j_5 = b + a * sin(e_d1 * 5 + f1);
    j_6 = b2 + a2 * sin(e_l1 * 6 + f2 + delta);

    j_7 = b + a * sin(e_d1 * 7 + f1);
    j_8 = b2 + a2 * sin(e_l1 * 8 + f2 + delta);

    j_9 = b + a * sin(e_d1 * 9 + f1);
    j_10 = b2 + a2 * sin(e_l1 * 10 + f2 + delta);

    j_11 = b + a * sin(e_d1 * 11 + f1);
    j_12 = b2 + a2 * sin(e_l1 * 12 + f2 + delta);

    j_13 = b + a * sin(e_d1 * 13 + f1);
    j_14 = b2 + a2 * sin(e_l1 * 14 + f2 + delta);

    j_15 = b + a * sin(e_d1 * 15 + f1);
    j_16 = b2 + a2 * sin(e_l1 * 16 + f2 + delta);


    joint_pos = [j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14, j_15, j_16];
end