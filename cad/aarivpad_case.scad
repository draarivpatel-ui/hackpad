// AarivPad - Parametric 3D-Printed Enclosure (OpenSCAD)
// Designed by Aariv Patel for Hack Club Stardance Hackpad Mission
// Total filament weight: ~58g PLA (well below 300g Printing Legion limit)

$fn = 48;

pcb_w = 68.0;
pcb_h = 84.0;
pcb_t = 1.6;
wall  = 3.0;
tol   = 0.4;

case_w = pcb_w + 2 * (wall + tol);
case_h = pcb_h + 2 * (wall + tol);
case_d = 14.0;

pitch = 19.05;
sw_cut = 14.0;

module rounded_box(w, h, d, r) {
    hull() {
        for (x = [r, w - r])
            for (y = [r, h - r])
                translate([x, y, 0])
                    cylinder(r = r, h = d);
    }
}

module bottom_case() {
    difference() {
        rounded_box(case_w, case_h, case_d, 4.0);
        // Inner cavity for PCB
        translate([wall, wall, 2.4])
            rounded_box(pcb_w + 2 * tol, pcb_h + 2 * tol, case_d, 1.5);
        // USB-C cutout for XIAO RP2040 at top-left
        translate([wall + tol + 11.0, case_h - wall - 1.0, 5.0])
            cube([11.0, wall + 2.0, 7.5]);
    }
    // 4x M2 standoff bosses
    for (mx = [wall + tol + 4.0, wall + tol + pcb_w - 4.0])
        for (my = [wall + tol + 4.0, wall + tol + pcb_h - 4.0])
            translate([mx, my, 2.4])
                difference() {
                    cylinder(r = 2.8, h = 4.5);
                    cylinder(r = 1.5, h = 5.0);
                }
}

module switch_plate() {
    difference() {
        rounded_box(case_w, case_h, 3.0, 4.0);
        // 3x3 MX Switch cutouts (14mm x 14mm on 19.05mm pitch)
        for (r = [0 : 2])
            for (c = [0 : 2]) {
                sx = wall + tol + 14.95 + c * pitch - sw_cut / 2;
                sy = wall + tol + (pcb_h - (34.95 + r * pitch)) - sw_cut / 2;
                translate([sx, sy, -0.5])
                    cube([sw_cut, sw_cut, 4.0]);
            }
        // OLED viewport window (top-center)
        translate([wall + tol + 25.0, wall + tol + pcb_h - 18.0, -0.5])
            cube([26.0, 12.0, 4.0]);
        // EC11 rotary encoder shaft cutout (top-right)
        translate([wall + tol + 56.0, wall + tol + pcb_h - 12.0, -0.5])
            cylinder(r = 4.2, h = 4.0);
        // 4x M2 screw holes
        for (mx = [wall + tol + 4.0, wall + tol + pcb_w - 4.0])
            for (my = [wall + tol + 4.0, wall + tol + pcb_h - 4.0])
                translate([mx, my, -0.5])
                    cylinder(r = 1.2, h = 4.0);
    }
}

module encoder_knob() {
    difference() {
        union() {
            cylinder(r1 = 9.0, r2 = 8.2, h = 13.5);
            translate([0, 0, 13.5])
                cylinder(r1 = 8.2, r2 = 7.2, h = 1.5);
        }
        // 6mm D-shaft bore
        translate([0, 0, -0.5])
            difference() {
                cylinder(r = 3.1, h = 11.5);
                translate([1.6, -4.0, 0])
                    cube([3.0, 8.0, 12.0]);
            }
        // Top indicator groove
        translate([-0.6, 2.0, 13.8])
            cube([1.2, 6.0, 2.0]);
    }
}

// Render preview assembly
bottom_case();
translate([0, 0, 16.0]) switch_plate();
translate([wall + tol + 56.0, wall + tol + pcb_h - 12.0, 20.0]) encoder_knob();
