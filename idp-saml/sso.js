document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const samlResponseForm = document.getElementById('samlResponseForm');
    const samlResponseInput = document.getElementById('SAMLResponse');
    const relayStateInput = document.getElementById('RelayState');

    const urlParams = new URLSearchParams(window.location.search);
    const samlRequest = urlParams.get('SAMLRequest');
    const relayState = urlParams.get('RelayState');

    if (!samlRequest) {
        alert('No SAMLRequest found.');
        return;
    }

    relayStateInput.value = relayState;

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username && password) {
            const samlAssertion = createSAMLAssertion(username);
            samlResponseInput.value = btoa(samlAssertion); // Base64 encode the SAML assertion
            samlResponseForm.action = relayState; // Set the form action to the SP's ACS URL
            samlResponseForm.submit();
        } else {
            alert('Please provide both username and password.');
        }
    });
});

function createSAMLAssertion(username) {
    const instant = new Date().toISOString();
    return `
        <saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
            <saml:Issuer>${issuer}</saml:Issuer>
            <saml:Subject>
                <saml:NameID>${username}</saml:NameID>
                <saml:SubjectConfirmation>
                    <saml:SubjectConfirmationData NotOnOrAfter="${new Date(Date.now() + 5 * 60 * 1000).toISOString()}" />
                </saml:SubjectConfirmation>
            </saml:Subject>
            <saml:Conditions NotBefore="${instant}" NotOnOrAfter="${new Date(Date.now() + 5 * 60 * 1000).toISOString()}">
            </saml:Conditions>
            <saml:AuthnStatement AuthnInstant="${instant}">
                <saml:AuthnContext>
                    <saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml:AuthnContextClassRef>
                </saml:AuthnContext>
            </saml:AuthnStatement>
        </saml:Assertion>
    `;
}
