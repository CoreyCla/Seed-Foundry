$(document).ready(function() {
//    window.submit_entry = function(attr_entry, prod) {
//
//		var attribute = document.getElementById(attr_entry);
//		var product = prod
//
//		var entry = {
//			attribute: name.value,
//			product: product.value
//		};
//
//		console.log(entry)
//	};
//
//	window.createMenus = function() {
//        var menuDiv = document.getElementById("product-attributes");
//        var attrs = {{ attr_items|tojson|safe }};
//
//        for (var attr in attrs) {
//            if (attrs.hasOwnProperty(attr)) {
//                console.log(attr + " -> " + attrs[attr]);
//            };
//
//            var selectList = document.createElement("select");
//            selectList.id = attrs;
//            menuDiv.appendChild(selectList);
//
//            for (var item in attrs[attr]) {
//                var finalAttrs = attrs[attr]
//                var option = document.createElement("option");
//
//                option.value = finalAttrs[item];
//                option.text = finalAttrs[item];
//                selectList.appendChild(option);
//            };
//        };
//    };
    function createMenus() {
        var menuDiv = document.getElementById("product-attributes");
        var attrs = {{attr_items|tojson|safe}};
        var selectList = document.createElement("select");

        for (var attr in attrs) {
            if (attrs.hasOwnProperty(attr)) {
                console.log(attr + " -> " + attrs[attr]);
            };

            selectList.id = attrs;
            menuDiv.appendChild(selectList);

            for (var item in attrs[attr]) {
                var finalAttrs = attrs[attr]
                var option = document.createElement("option");

                option.value = finalAttrs[item];
                option.text = finalAttrs[item];
                selectList.appendChild(option);
            };
        };
    };
});

