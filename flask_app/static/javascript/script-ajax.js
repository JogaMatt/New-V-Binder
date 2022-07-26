const button = document.querySelectorAll('#check_out')

function pay(element) {
    fetch('/stripe_pay')
    .then((result) => { return result.json()})
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key)
        stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
        }).then(function (result) {

        });
    })
};