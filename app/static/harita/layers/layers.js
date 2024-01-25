var wms_layers = [];


        var lyr_OpenStreetMap_0 = new ol.layer.Tile({
            'title': 'Open Street Map',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' ',
                url: 'http://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var format_harita_1 = new ol.format.GeoJSON();
var features_harita_1 = format_harita_1.readFeatures(json_harita_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_harita_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_harita_1.addFeatures(features_harita_1);
var lyr_harita_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_harita_1, 
                style: style_harita_1,
                interactive: true,
                title: ' '
            });
var group_BAGCILAR_KDSncz = new ol.layer.Group({
                                layers: [lyr_harita_1,],
                                title: "BAGCILAR_KDS.ncz"});
var group_BaseMaps = new ol.layer.Group({
                                layers: [lyr_OpenStreetMap_0,],
                                title: "BaseMaps"});

lyr_OpenStreetMap_0.setVisible(true);lyr_harita_1.setVisible(true);
var layersList = [group_BaseMaps,group_BAGCILAR_KDSncz];
lyr_harita_1.set('fieldAliases', {'id': 'id', 'oda_id': 'oda_id', 'geom_type': 'geom_type', 'line_thickness': 'line_thickness', 'line_type': 'line_type', 'color_code': 'color_code', 'thickness': 'thickness', 'factor': 'factor', 'text_data': 'text_data', 'object_properties': 'object_properties', 'point_height': 'point_height', 'length': 'length', 'ybizden': 'ybizden', 'ortahasar': 'ortahasar', });
lyr_harita_1.set('fieldImages', {'id': 'TextEdit', 'oda_id': 'TextEdit', 'geom_type': 'TextEdit', 'line_thickness': 'TextEdit', 'line_type': 'TextEdit', 'color_code': 'TextEdit', 'thickness': 'TextEdit', 'factor': 'TextEdit', 'text_data': 'TextEdit', 'object_properties': 'TextEdit', 'point_height': 'TextEdit', 'length': 'TextEdit', 'ybizden': 'TextEdit', 'ortahasar': 'TextEdit', });
lyr_harita_1.set('fieldLabels', {});
lyr_harita_1.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});