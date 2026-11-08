import 'package:flutter/material.dart';



// ======================================================================
// EVA LOTUS LOGO
// ======================================================================
//
// Clean 5-petal EVA logo.
// No external assets.
// No dart:ui.
// Works directly with Flutter Canvas.
// ======================================================================

class EvaLogoPainter extends CustomPainter {
  const EvaLogoPainter();

  @override
  void paint(Canvas canvas, Size size) {
    final double w = size.width;
    final double h = size.height;

    final Offset center = Offset(
      w / 2,
      h / 2,
    );

    // ================================================================
    // MAIN GRADIENT
    // ================================================================

    final Paint purplePaint = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          Color(0xFFE08AFF),
          Color(0xFFB35CFF),
          Color(0xFF8655FF),
        ],
      ).createShader(
        Rect.fromLTWH(0, 0, w, h),
      )
      ..style = PaintingStyle.fill
      ..isAntiAlias = true;

    // ================================================================
    // LOWER PETAL GRADIENT
    // ================================================================

    final Paint lowerPaint = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          Color(0xFF9A62FF),
          Color(0xFF6878FF),
          Color(0xFF536DFF),
        ],
      ).createShader(
        Rect.fromLTWH(0, h * 0.38, w, h * 0.42),
      )
      ..style = PaintingStyle.fill
      ..isAntiAlias = true;

    // ================================================================
    // CENTER PETAL
    // ================================================================

    final Path centerPetal = Path();

    centerPetal.moveTo(
      center.dx,
      h * 0.08,
    );

    centerPetal.cubicTo(
      w * 0.37,
      h * 0.20,
      w * 0.33,
      h * 0.40,
      center.dx,
      h * 0.60,
    );

    centerPetal.cubicTo(
      w * 0.67,
      h * 0.40,
      w * 0.63,
      h * 0.20,
      center.dx,
      h * 0.08,
    );

    centerPetal.close();

    canvas.drawPath(
      centerPetal,
      purplePaint,
    );

    // ================================================================
    // LEFT UPPER PETAL
    // ================================================================

    final Path leftPetal = Path();

    leftPetal.moveTo(
      center.dx,
      h * 0.61,
    );

    leftPetal.cubicTo(
      w * 0.39,
      h * 0.55,
      w * 0.19,
      h * 0.43,
      w * 0.17,
      h * 0.27,
    );

    leftPetal.cubicTo(
      w * 0.36,
      h * 0.28,
      w * 0.49,
      h * 0.43,
      center.dx,
      h * 0.61,
    );

    leftPetal.close();

    canvas.drawPath(
      leftPetal,
      purplePaint,
    );

    // ================================================================
    // RIGHT UPPER PETAL
    // ================================================================

    final Path rightPetal = Path();

    rightPetal.moveTo(
      center.dx,
      h * 0.61,
    );

    rightPetal.cubicTo(
      w * 0.61,
      h * 0.55,
      w * 0.81,
      h * 0.43,
      w * 0.83,
      h * 0.27,
    );

    rightPetal.cubicTo(
      w * 0.64,
      h * 0.28,
      w * 0.51,
      h * 0.43,
      center.dx,
      h * 0.61,
    );

    rightPetal.close();

    canvas.drawPath(
      rightPetal,
      purplePaint,
    );

    // ================================================================
    // LOWER LEFT PETAL
    // ================================================================

    final Path lowerLeft = Path();

    lowerLeft.moveTo(
      center.dx,
      h * 0.67,
    );

    lowerLeft.cubicTo(
      w * 0.40,
      h * 0.67,
      w * 0.19,
      h * 0.62,
      w * 0.09,
      h * 0.49,
    );

    lowerLeft.cubicTo(
      w * 0.30,
      h * 0.46,
      w * 0.48,
      h * 0.53,
      center.dx,
      h * 0.67,
    );

    lowerLeft.close();

    canvas.drawPath(
      lowerLeft,
      lowerPaint,
    );

    // ================================================================
    // LOWER RIGHT PETAL
    // ================================================================

    final Path lowerRight = Path();

    lowerRight.moveTo(
      center.dx,
      h * 0.67,
    );

    lowerRight.cubicTo(
      w * 0.60,
      h * 0.67,
      w * 0.81,
      h * 0.62,
      w * 0.91,
      h * 0.49,
    );

    lowerRight.cubicTo(
      w * 0.70,
      h * 0.46,
      w * 0.52,
      h * 0.53,
      center.dx,
      h * 0.67,
    );

    lowerRight.close();

    canvas.drawPath(
      lowerRight,
      lowerPaint,
    );

    // ================================================================
    // SUBTLE CENTER GLOW
    // ================================================================

    final Paint centerGlow = Paint()
      ..color = const Color(0x229E65FF)
      ..style = PaintingStyle.fill
      ..maskFilter = const MaskFilter.blur(
        BlurStyle.normal,
        3,
      );

    canvas.drawCircle(
      Offset(center.dx, h * 0.61),
      w * 0.06,
      centerGlow,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}