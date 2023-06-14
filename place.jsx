var inputFile = File("C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/output.txt");

if (inputFile.open("r")) {
    //alert("File opened successfully");

    var originalRulerUnits = app.preferences.rulerUnits;
    app.preferences.rulerUnits = Units.PIXELS;

    var docWidth = 100;
    var docHeight = 100;
    var doc = app.documents.add(docWidth, docHeight, 72, 'output', NewDocumentMode.RGB, DocumentFill.TRANSPARENT);

    var idx = 0;
    while (!inputFile.eof) {
        var line = inputFile.readln();
        var parts = line.split(":");
        if (parts.length == 2) {
            var values = parts[1].split(",");
            var x = parseFloat(values[0].split("=")[1]);
            var y = parseFloat(values[1].split("=")[1]);
            var scale = parseFloat(values[2].split("=")[1]);

            // Transform coordinates
            x = (x - (docWidth / 2))*1;
            y = (y - (docHeight / 2))*1;

            //alert("Transformed x=" + x + ", y=" + y + ", scale=" + scale);

            var imageFile = new File("C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/images/" + (idx < 10 ? '0' : '') + idx + ".png");

            if (imageFile.exists) {
                var imageLayer = doc.artLayers.add();
                imageLayer.kind = LayerKind.NORMAL;
                imageLayer.name = "Image" + idx;

                app.open(imageFile);
                app.activeDocument.selection.selectAll();
                app.activeDocument.selection.copy();
                app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);

                app.activeDocument = doc;
                doc.paste();

                var layer = doc.artLayers[0];

                
                var layerWidth = layer.bounds[2] - layer.bounds[0];
                var layerHeight = layer.bounds[3] - layer.bounds[1];
                var centerX = 0;
                var centerY = 0;
                if (layerWidth > docWidth){
                    var centerX = (layerWidth - docWidth) / -2;
                }
                if (layerHeight > docHeight){
                    var centerY = (layerHeight- docHeight) / -2;
                }

                layer.translate(UnitValue(centerX, "px"), UnitValue(centerY, "px"));

                // Move the layer to the appropriate position
                var deltaX = x + ((layer.bounds[2] - layer.bounds[0]) / 2)*scale;
                var deltaY = y + ((layer.bounds[3] - layer.bounds[1]) / 2)*scale;
                layer.translate(UnitValue(deltaX, "px"), UnitValue(deltaY*-1, "px"));

                // Scale the layer
                layer.resize(scale * 100, scale * 100, AnchorPosition.MIDDLECENTER);

                idx++;
            } else {
                alert("Image file does not exist: " + imageFile);
            }
        }
    }
    inputFile.close();
    
    // Restore the original ruler units
    app.preferences.rulerUnits = originalRulerUnits;

} else {
    alert("Failed to open file");
}
