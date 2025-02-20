odoo.define('it_procurement.purchase_approval', function (require) {
    'use strict';

    var ajax = require('web.ajax');

    $(document).ready(function () {
        $('.approve-btn').click(function () {
            var orderId = $(this).data('order-id');
            ajax.jsonRpc('/it_procurement/approve_purchase/' + orderId, 'call', {})
                .then(function (result) {
                    if (result.status === 'success') {
                        location.reload();
                    } else {
                        alert(result.message);
                    }
                });
        });
    });
});