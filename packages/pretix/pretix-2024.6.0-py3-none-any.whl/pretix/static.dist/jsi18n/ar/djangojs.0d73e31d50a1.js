

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "(one more date)": [
      "\u0648\u0644\u0627 \u064a\u0648\u0645",
      "\u064a\u0648\u0645 \u0648\u0627\u062d\u062f",
      "\u064a\u0648\u0645\u0627\u0646",
      "\u0623\u064a\u0627\u0645",
      "\u0623\u064a\u0627\u0645 \u0639\u062f\u064a\u062f\u0629",
      "\u0623\u062e\u0631\u0649"
    ],
    "Add condition": "\u0623\u0636\u0641 \u0634\u0631\u0637\u0627",
    "Additional information required": "\u0645\u0637\u0644\u0648\u0628 \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0625\u0636\u0627\u0641\u064a\u0629",
    "All": "\u0627\u0644\u0643\u0644",
    "All of the conditions below (AND)": "\u062c\u0645\u064a\u0639 \u0627\u0644\u0634\u0631\u0648\u0637 \u0641\u064a \u0627\u0644\u0623\u0633\u0641\u0644",
    "An error has occurred.": "\u062d\u062f\u062b \u062e\u0637\u0623.",
    "An error of type {code} occurred.": "\u062d\u062f\u062b \u062e\u0637\u0623 \u0645\u0646 \u0646\u0648\u0639 {code}.",
    "April": "\u0623\u0628\u0631\u064a\u0644",
    "At least one of the conditions below (OR)": "\u062e\u064a\u0627\u0631 \u0648\u0627\u062d\u062f \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644",
    "August": "\u0623\u063a\u0633\u0637\u0633",
    "Barcode area": "\u0645\u0646\u0637\u0642\u0629 \u0628\u0627\u0631\u0643\u0648\u062f",
    "Calculating default price\u2026": "\u062d\u0633\u0627\u0628 \u0627\u0644\u0633\u0639\u0631 \u0627\u0644\u0627\u0641\u062a\u0631\u0627\u0636\u064a\u2026",
    "Cancel": "\u0642\u0645 \u0628\u0627\u0644\u0625\u0644\u063a\u0627\u0621",
    "Canceled": "\u0645\u0644\u063a\u0627\u0629",
    "Cart expired": "\u0627\u0646\u062a\u0647\u062a \u0635\u0644\u0627\u062d\u064a\u0629 \u0639\u0631\u0628\u0629 \u0627\u0644\u062a\u0633\u0648\u0642",
    "Check-in QR": "QR \u0627\u0644\u062f\u062e\u0648\u0644",
    "Checked-in Tickets": "\u062a\u0630\u0627\u0643\u0631 \u0627\u0644\u062f\u062e\u0648\u0644",
    "Click to close": "\u0627\u0636\u063a\u0637 \u0644\u0627\u063a\u0644\u0627\u0642 \u0627\u0644\u0635\u0641\u062d\u0629",
    "Close message": "\u0623\u063a\u0644\u0642 \u0627\u0644\u0631\u0633\u0627\u0644\u0629",
    "Comment:": "\u062a\u0639\u0644\u064a\u0642:",
    "Confirming your payment \u2026": "\u062c\u0627\u0631\u064a \u062a\u0623\u0643\u064a\u062f \u0627\u0644\u062f\u0641\u0639 \u0627\u0644\u062e\u0627\u0635 \u0628\u0643 \u2026",
    "Contacting Stripe \u2026": "\u062c\u0627\u0631\u064a \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628Stripe \u2026",
    "Contacting your bank \u2026": "\u062c\u0627\u0631\u064a \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u0627\u0644\u0628\u0646\u0643 \u0627\u0644\u0630\u064a \u062a\u062a\u0639\u0627\u0645\u0644 \u0645\u0639\u0647 \u2026",
    "Continue": "\u0627\u0644\u0645\u062a\u0627\u0628\u0639\u0629",
    "Copied!": "\u062a\u0645 \u0627\u0644\u0646\u0633\u062e!",
    "Count": "\u0627\u062d\u0633\u0628",
    "Current date and time": "\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648\u0627\u0644\u0648\u0642\u062a \u0627\u0644\u062d\u0627\u0644\u064a",
    "Currently inside": "\u062d\u0627\u0644\u064a\u0627 \u0628\u0627\u0644\u062f\u0627\u062e\u0644",
    "December": "\u062f\u064a\u0633\u0645\u0628\u0631",
    "Do you really want to leave the editor without saving your changes?": "\u0647\u0644 \u062a\u0631\u064a\u062f \u0623\u0646 \u062a\u063a\u0627\u062f\u0631 \u0627\u0644\u0645\u062d\u0631\u0631 \u062f\u0648\u0646 \u062d\u0641\u0638 \u0627\u0644\u062a\u0639\u062f\u064a\u0644\u0627\u062a\u061f",
    "Entry": "\u062f\u062e\u0648\u0644",
    "Entry not allowed": "\u0625\u062f\u062e\u0627\u0644 \u063a\u064a\u0631 \u0645\u0633\u0645\u0648\u062d",
    "Error while uploading your PDF file, please try again.": "\u062d\u0635\u0644 \u062e\u0637\u0623 \u0623\u062b\u0646\u0627\u0621 \u0631\u0641\u0639 \u0645\u0644\u0641 PDF \u0627\u0644\u062e\u0627\u0635 \u0628\u0643\u060c \u064a\u0631\u062c\u0649 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649.",
    "Event admission": "\u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u0641\u0639\u0627\u0644\u064a\u0629",
    "Event end": "\u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0641\u0639\u0627\u0644\u064a\u0629",
    "Event start": "\u0628\u062f\u0627\u064a\u0629 \u0627\u0644\u0641\u0639\u0627\u0644\u064a\u0629",
    "Exit": "\u062e\u0631\u0648\u062c",
    "Exit recorded": "\u062a\u0645 \u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u062e\u0631\u0648\u062c",
    "February": "\u0641\u0628\u0631\u0627\u064a\u0631",
    "Fr": "\u0627\u0644\u062c\u0645\u0639\u0629",
    "Generating messages \u2026": "\u062a\u0648\u0644\u064a\u062f \u0627\u0644\u0631\u0633\u0627\u0626\u0644 \u2026",
    "Group of objects": "\u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u0646 \u0627\u0644\u0639\u0646\u0627\u0635\u0631",
    "Image area": "\u0645\u0646\u0637\u0642\u0629 \u0635\u0648\u0631\u0629",
    "Information required": "\u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0645\u0637\u0644\u0648\u0628\u0629",
    "January": "\u064a\u0646\u0627\u064a\u0631",
    "July": "\u064a\u0648\u0644\u064a\u0648",
    "June": "\u064a\u0648\u0646\u064a\u0648",
    "Load more": "\u062a\u062d\u0645\u064a\u0644 \u0627\u0644\u0645\u0632\u064a\u062f",
    "March": "\u0645\u0627\u0631\u0633",
    "Marked as paid": "\u0637\u0644\u0628\u0627\u062a \u0645\u0643\u062a\u0645\u0644\u0629",
    "May": "\u0645\u0627\u064a\u0648",
    "Mo": "\u0627\u0644\u0625\u062b\u0646\u064a\u0646",
    "No": "\u0644\u0627",
    "No active check-in lists found.": "\u0644\u0645 \u064a\u062a\u0645 \u0627\u0644\u0639\u062b\u0648\u0631 \u0639\u0644\u0649 \u0642\u0648\u0627\u0626\u0645 \u062f\u062e\u0648\u0644 \u0646\u0634\u0637\u0629.",
    "No tickets found": "\u0644\u0645 \u064a\u062a\u0645 \u0627\u0644\u0639\u062b\u0648\u0631 \u0639\u0644\u0649 \u062a\u0630\u0627\u0643\u0631",
    "None": "\u0644\u0627 \u0634\u064a\u0621",
    "November": "\u0646\u0648\u0641\u0645\u0628\u0631",
    "Number of days with a previous entry": "\u0639\u062f\u062f \u0627\u0644\u0623\u064a\u0627\u0645 \u0627\u0644\u062a\u064a \u062a\u062d\u062a\u0648\u064a \u0639\u0644\u0649 \u0645\u062f\u062e\u0644 \u0633\u0627\u0628\u0642",
    "Number of previous entries": "\u0639\u062f\u062f \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a \u0627\u0644\u0633\u0627\u0628\u0642\u0629",
    "Number of previous entries since midnight": "\u0639\u062f\u062f \u0627\u0644\u0645\u062f\u062e\u0644\u0627\u062a \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0642\u0628\u0644 \u0645\u0646\u062a\u0635\u0641 \u0627\u0644\u0644\u064a\u0644",
    "Object": "\u0639\u0646\u0635\u0631",
    "October": "\u0623\u0643\u062a\u0648\u0628\u0631",
    "Order canceled": "\u062a\u0645 \u0625\u0644\u063a\u0627\u0621 \u0627\u0644\u0637\u0644\u0628",
    "Others": "\u063a\u064a\u0631 \u0630\u0644\u0643",
    "Paid orders": "\u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0645\u062f\u0641\u0648\u0639\u0629",
    "Placed orders": "\u0637\u0644\u0628\u0627\u062a \u0645\u062e\u062a\u0627\u0631\u0629",
    "Please enter a quantity for one of the ticket types.": "\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u062f\u062e\u0627\u0644 \u0639\u062f\u062f \u0644\u0623\u062d\u062f \u0623\u0646\u0648\u0627\u0639 \u0627\u0644\u062a\u0630\u0627\u0643\u0631.",
    "Please enter the amount the organizer can keep.": "\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u062f\u062e\u0627\u0644 \u0627\u0644\u0645\u0628\u0644\u063a \u0627\u0644\u0630\u064a \u064a\u0645\u0643\u0646 \u0644\u0644\u0645\u0646\u0638\u0645 \u0627\u0644\u0627\u062d\u062a\u0641\u0627\u0638 \u0628\u0647.",
    "Powered by pretix": "\u0645\u062f\u0639\u0648\u0645 \u0645\u0646 pretix",
    "Press Ctrl-C to copy!": "\u0644\u0644\u0646\u0633\u062e \u0627\u0636\u063a\u0637 Ctrl + C!",
    "Product": "\u0645\u0646\u062a\u062c",
    "Product variation": "\u0646\u0648\u0639 \u0627\u0644\u0645\u0646\u062a\u062c",
    "Redeemed": "\u0645\u0633\u062a\u062e\u062f\u0645",
    "Result": "\u0627\u0644\u0646\u062a\u064a\u062c\u0629",
    "Sa": "\u0627\u0644\u0633\u0628\u062a",
    "Saving failed.": "\u0641\u0634\u0644\u062a \u0639\u0645\u0644\u064a\u0629 \u0627\u0644\u062d\u0641\u0638.",
    "Scan a ticket or search and press return\u2026": "\u0642\u0645 \u0628\u0645\u0633\u062d \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u0623\u0648 \u0625\u0628\u062d\u062b \u0648\u0627\u0636\u063a\u0637 \u0632\u0631 \u0627\u0644\u0639\u0648\u062f\u0629\u2026",
    "Search query": "\u0627\u0644\u0628\u062d\u062b \u0641\u064a \u0627\u0644\u0627\u0633\u062a\u0641\u0633\u0627\u0631\u0627\u062a",
    "Search results": "\u0627\u0644\u0628\u062d\u062b \u0641\u064a \u0627\u0644\u0646\u062a\u0627\u0626\u062c",
    "Select a check-in list": "\u0627\u062e\u062a\u0631 \u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u062f\u062e\u0648\u0644",
    "Selected only": "\u0627\u0644\u0645\u062e\u062a\u0627\u0631\u0629 \u0641\u0642\u0637",
    "September": "\u0633\u0628\u062a\u0645\u0628\u0631",
    "Su": "\u0627\u0644\u0623\u062d\u062f",
    "Switch check-in list": "\u062a\u0628\u062f\u064a\u0644 \u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u062f\u062e\u0648\u0644",
    "Switch direction": "\u062a\u063a\u064a\u064a\u0631 \u0627\u0644\u0645\u0633\u0627\u0631",
    "Text object": "\u0639\u0646\u0635\u0631 \u0646\u0635",
    "Th": "\u0627\u0644\u062e\u0645\u064a\u0633",
    "The PDF background file could not be loaded for the following reason:": "\u0644\u0627 \u064a\u0645\u0643\u0646 \u062a\u062d\u0645\u064a\u0644 \u0645\u0644\u0641 PDF \u0627\u0644\u062e\u0644\u0641\u064a\u0629 \u0644\u0644\u0623\u0633\u0628\u0627\u0628 \u0627\u0644\u062a\u0627\u0644\u064a\u0629:",
    "The organizer keeps %(currency)s %(amount)s": "\u064a\u062d\u0635\u0644 \u0627\u0644\u0645\u0646\u0638\u0645 \u0639\u0644\u0649 %(currency) %(amount)",
    "The request took too long. Please try again.": "\u0627\u0633\u062a\u063a\u0631\u0642\u062a \u0627\u0644\u0637\u0644\u0628 \u0641\u062a\u0631\u0629 \u0637\u0648\u064a\u0644\u0629\u060c \u0627\u0644\u0631\u062c\u0627\u0621 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649.",
    "This ticket is not yet paid. Do you want to continue anyways?": "\u0644\u0645 \u064a\u062a\u0645 \u062f\u0641\u0639 \u0642\u064a\u0645\u0629 \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u0628\u0639\u062f\u060c \u0647\u0644 \u062a\u0631\u064a\u062f \u0627\u0644\u0645\u062a\u0627\u0628\u0639\u0629 \u0639\u0644\u0649 \u0623\u064a \u062d\u0627\u0644\u061f",
    "This ticket requires special attention": "\u062a\u062d\u062a\u0627\u062c \u0647\u0630\u0647 \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u0625\u0644\u0649 \u0625\u0647\u062a\u0645\u0627\u0645 \u062e\u0627\u0635",
    "Ticket already used": "\u062a\u0645 \u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u0645\u0633\u0628\u0642\u0627",
    "Ticket code revoked/changed": "\u062a\u0645 \u0625\u0644\u063a\u0627\u0621 \u0631\u0645\u0632 \u0627\u0644\u062a\u0630\u0643\u0631\u0629 \u0623\u0648 \u062a\u0628\u062f\u064a\u0644\u0647",
    "Ticket design": "\u062a\u0635\u0645\u064a\u0645 \u0627\u0644\u062a\u0630\u0643\u0631\u0629",
    "Ticket not paid": "\u0644\u0645 \u064a\u062a\u0645 \u062f\u0641\u0639 \u0642\u064a\u0645\u0629 \u0627\u0644\u062a\u0630\u0643\u0631\u0629",
    "Time zone:": "\u0627\u0644\u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u0632\u0645\u0646\u064a\u0629:",
    "Tolerance (minutes)": "\u0627\u0644\u0642\u062f\u0631\u0629 \u0639\u0644\u0649 \u0627\u0644\u062a\u062d\u0645\u0644 (\u0627\u0644\u062f\u0642\u0627\u0626\u0642)",
    "Total": "\u0627\u0644\u0645\u062c\u0645\u0648\u0639",
    "Total revenue": "\u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0625\u064a\u0631\u0627\u062f\u0627\u062a",
    "Tu": "\u0627\u0644\u062b\u0644\u0627\u062b\u0627\u0621",
    "Unknown error.": "\u062e\u0637\u0623 \u063a\u064a\u0631 \u0645\u0639\u0631\u0648\u0641.",
    "Unpaid": "\u063a\u064a\u0631 \u0645\u062f\u0641\u0648\u0639",
    "Use a different name internally": "\u0642\u0645 \u0628\u0627\u0633\u062a\u062e\u062f\u0645 \u0627\u0633\u0645 \u0645\u062e\u062a\u0644\u0641 \u062f\u0627\u062e\u0644\u064a\u0627",
    "Valid": "\u0633\u0627\u0631\u064a \u0627\u0644\u0645\u0641\u0639\u0648\u0644",
    "Valid Tickets": "\u062a\u0630\u0627\u0643\u0631 \u0633\u0627\u0631\u064a\u0629 \u0627\u0644\u0645\u0641\u0639\u0648\u0644",
    "Valid ticket": "\u062a\u0630\u0643\u0631\u0629 \u0633\u0627\u0631\u064a\u0629 \u0627\u0644\u0645\u0641\u0639\u0648\u0644",
    "We": "\u0627\u0644\u0623\u0631\u0628\u0639\u0627\u0621",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "\u0646\u0639\u0645\u0644 \u0627\u0644\u0622\u0646 \u0639\u0644\u0649 \u0627\u0631\u0633\u0627\u0644 \u0637\u0644\u0628\u0643 \u0625\u0644\u0649 \u0627\u0644\u062e\u0627\u062f\u0645\u060c \u0625\u0630\u0627 \u0623\u0633\u062a\u063a\u0631\u0642\u062a \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0623\u0643\u062b\u0631 \u0645\u0646 \u062f\u0642\u064a\u0642\u0629\u060c \u064a\u0631\u062c\u0649 \u0627\u0644\u062a\u062d\u0642\u0642 \u0645\u0646 \u0627\u062a\u0635\u0627\u0644\u0643 \u0628\u0627\u0644\u0625\u0646\u062a\u0631\u0646\u062a \u062b\u0645 \u0623\u0639\u062f \u062a\u062d\u0645\u064a\u0644 \u0627\u0644\u0635\u0641\u062d\u0629 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649.",
    "We are processing your request \u2026": "\u062c\u0627\u0631\u064a \u0645\u0639\u0627\u0644\u062c\u0629 \u0637\u0644\u0628\u0643 \u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "\u0644\u0645 \u0646\u062a\u0645\u0643\u0646 \u0645\u0646 \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u0627\u0644\u062e\u0627\u062f\u0645\u060c \u0644\u0643\u0646 \u0633\u0646\u0648\u0627\u0635\u0644 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629\u060c \u0631\u0645\u0632 \u0622\u062e\u0631 \u062e\u0637\u0623: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "\u0644\u0627 \u064a\u0645\u0643\u0646\u0646\u0627 \u0627\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u0649 \u0627\u0644\u062e\u0627\u062f\u0645 \u062d\u0627\u0644\u064a\u0627\u060c \u062d\u0627\u0648\u0644 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649 \u0645\u0646 \u0641\u0636\u0644\u0643. \u0631\u0645\u0632 \u0627\u0644\u062e\u0637\u0623 : {code}",
    "Yes": "\u0646\u0639\u0645",
    "You get %(currency)s %(amount)s back": "\u0633\u062a\u0633\u062a\u0631\u062f %(currency)%(amount)",
    "You have unsaved changes!": "\u0644\u0645 \u062a\u0642\u0645 \u0628\u062d\u0641\u0638 \u0627\u0644\u062a\u0639\u062f\u064a\u0644\u0627\u062a!",
    "Your color has bad contrast for text on white background, please choose a darker shade.": "\u062a\u0628\u0627\u064a\u0646 \u0627\u0644\u0644\u0648\u0646 \u0633\u064a\u0626 \u0644\u0644\u062e\u0644\u0641\u064a\u0629 \u0627\u0644\u0628\u064a\u0636\u0627\u0621\u060c \u0627\u0644\u0631\u062c\u0627\u0621 \u0627\u062e\u062a\u064a\u0627\u0631 \u0644\u0648\u0646 \u063a\u0627\u0645\u0642.",
    "Your color has decent contrast and is probably good-enough to read!": "\u0627\u0644\u0644\u0648\u0646 \u064a\u062d\u0638\u0649 \u0628\u062a\u0628\u0627\u064a\u0646 \u0645\u0639\u0642\u0648\u0644 \u0648\u064a\u0645\u0643\u0646 \u0623\u0646 \u064a\u0643\u0648\u0646 \u0645\u0646\u0627\u0633\u0628 \u0644\u0644\u0642\u0631\u0627\u0621\u0629!",
    "Your color has great contrast and is very easy to read!": "\u0627\u0644\u0644\u0648\u0646 \u064a\u062a\u0645\u062a\u0639 \u0628\u062a\u0628\u0627\u064a\u0646 \u0643\u0628\u064a\u0631 \u0648\u062a\u0633\u0647\u0644 \u0642\u0631\u0627\u0621\u062a\u0647!",
    "Your local time:": "\u0627\u0644\u062a\u0648\u0642\u064a\u062a \u0627\u0644\u0645\u062d\u0644\u064a:",
    "Your request arrived on the server but we still wait for it to be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "\u0648\u0635\u0644 \u0637\u0644\u0628\u0643 \u0644\u0644\u062e\u0627\u062f\u0645 \u0648\u0646\u0646\u062a\u0638\u0631 \u062a\u0646\u0641\u064a\u0630\u0647. \u0625\u0630\u0627 \u0627\u0633\u062a\u063a\u0631\u0642 \u0627\u0644\u0623\u0645\u0631 \u0623\u0643\u062b\u0631 \u0645\u0646 \u062f\u0642\u064a\u0642\u062a\u064a\u0646 \u062a\u0648\u0627\u0635\u0644 \u0645\u0639\u0646\u0627 \u0623\u0648 \u0639\u0627\u0648\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0645\u062c\u062f\u062f\u0627.",
    "Your request has been queued on the server and will soon be processed.": "\u0637\u0644\u0628\u0643 \u0642\u064a\u062f \u0627\u0644\u0627\u0646\u062a\u0638\u0627\u0631 \u0648\u0633\u062a\u062a\u0645 \u0645\u0639\u0627\u0644\u062c\u062a\u0647 \u0642\u0631\u064a\u0628\u0627.",
    "Your request is currently being processed. Depending on the size of your event, this might take up to a few minutes.": "\u062a\u062a\u0645 \u0645\u0639\u0627\u0644\u062c\u0629 \u0637\u0644\u0628\u0643 \u062d\u0627\u0644\u064a\u0627. \u0642\u062f \u064a\u0633\u062a\u063a\u0631\u0642 \u0627\u0644\u0623\u0645\u0631 \u0628\u0636\u0639 \u062f\u0642\u0627\u0626\u0642 \u0628\u0646\u0627\u0621 \u0639\u0644\u0649 \u062d\u062c\u0645 \u0627\u0644\u0641\u0639\u0627\u0644\u064a\u0629 \u0627\u0644\u062a\u064a \u0627\u062e\u062a\u0631\u062a.",
    "custom date and time": "\u062a\u062d\u062f\u064a\u062f \u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648\u0627\u0644\u0648\u0642\u062a",
    "custom time": "\u0627\u0644\u0648\u0642\u062a \u0627\u0644\u0645\u062d\u062f\u062f",
    "is after": "\u0628\u0639\u062f",
    "is before": "\u0642\u0628\u0644",
    "is one of": "\u0648\u0627\u062d\u062f \u0645\u0646",
    "minutes": "\u0627\u0644\u062f\u0642\u0627\u0626\u0642",
    "required": "\u0645\u0637\u0644\u0648\u0628",
    "widget\u0004Back": "\u0627\u0644\u0639\u0648\u062f\u0629",
    "widget\u0004Buy": "\u0627\u0634\u062a\u0631\u064a",
    "widget\u0004Choose a different date": "\u0627\u062e\u062a\u0631 \u062a\u0627\u0631\u064a\u062e\u0627 \u0622\u062e\u0631",
    "widget\u0004Choose a different event": "\u0627\u062e\u062a\u0631 \u0641\u0639\u0627\u0644\u064a\u0629 \u0623\u062e\u0631\u0649",
    "widget\u0004Close": "\u0625\u063a\u0644\u0627\u0642",
    "widget\u0004Close ticket shop": "\u0625\u063a\u0644\u0627\u0642 \u0645\u062a\u062c\u0631 \u0627\u0644\u062a\u0630\u0627\u0643\u0631",
    "widget\u0004Continue": "\u0627\u0633\u062a\u0645\u0631\u0627\u0631",
    "widget\u0004FREE": "\u0645\u062c\u0627\u0646\u064a",
    "widget\u0004Next month": "\u0627\u0644\u0634\u0647\u0631 \u0627\u0644\u0642\u0627\u062f\u0645",
    "widget\u0004Next week": "\u0627\u0644\u0623\u0633\u0628\u0648\u0639 \u0627\u0644\u0642\u0627\u062f\u0645",
    "widget\u0004Only available with a voucher": "\u0645\u062a\u0648\u0641\u0631\u0629 \u0645\u0639 \u0627\u0644\u0642\u0633\u064a\u0645\u0629 \u0641\u0642\u0637",
    "widget\u0004Open seat selection": "\u062e\u064a\u0627\u0631\u0627\u062a \u0627\u0644\u0645\u0642\u0627\u0639\u062f",
    "widget\u0004Previous month": "\u0627\u0644\u0634\u0647\u0631 \u0627\u0644\u0633\u0627\u0628\u0642",
    "widget\u0004Previous week": "\u0627\u0644\u0623\u0633\u0628\u0648\u0639 \u0627\u0644\u0633\u0627\u0628\u0642",
    "widget\u0004Redeem": "\u0627\u0633\u062a\u0628\u062f\u0627\u0644",
    "widget\u0004Redeem a voucher": "\u0627\u0633\u062a\u0628\u062f\u0627\u0644 \u0642\u0633\u064a\u0645\u0629",
    "widget\u0004Register": "\u0633\u062c\u0644",
    "widget\u0004Reserved": "\u0645\u062d\u062c\u0648\u0632",
    "widget\u0004Resume checkout": "\u0627\u0633\u062a\u0626\u0646\u0627\u0641 \u0627\u0644\u062f\u0641\u0639",
    "widget\u0004Sold out": "\u062a\u0645 \u0627\u0644\u0628\u064a\u0639 \u0628\u0627\u0644\u0643\u0627\u0645\u0644",
    "widget\u0004The cart could not be created. Please try again later": "\u0644\u0627 \u064a\u0645\u0643\u0646 \u0625\u0646\u0634\u0627\u0621 \u0633\u0644\u0629 \u0627\u0644\u062a\u0633\u0648\u0642. \u0627\u0644\u0631\u062c\u0627\u0621 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649 \u0641\u064a \u0648\u0642\u062a \u0644\u0627\u062d\u0642",
    "widget\u0004The ticket shop could not be loaded.": "\u0644\u0627 \u064a\u0645\u0643\u0646 \u062a\u062d\u0645\u064a\u0644 \u0645\u062a\u062c\u0631 \u0627\u0644\u062a\u0630\u0627\u0643\u0631.",
    "widget\u0004Voucher code": "\u0631\u0645\u0632 \u0627\u0644\u0642\u0633\u064a\u0645\u0629",
    "widget\u0004Waiting list": "\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u0625\u0646\u062a\u0638\u0627\u0631",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "\u0644\u062f\u064a\u0643 \u0627\u0644\u0622\u0646 \u0633\u0644\u0629 \u062a\u0633\u0648\u0642 \u0645\u0641\u0639\u0644\u0629 \u0644\u0647\u0630\u0627 \u0627\u0644\u062d\u062f\u062b. \u0625\u0630\u0627 \u0642\u0645\u062a \u0628\u0627\u062e\u062a\u064a\u0627\u0631 \u0645\u0646\u062a\u062c\u0627\u062a \u0623\u062e\u0631\u0649 \u0633\u064a\u062a\u0645 \u0625\u0636\u0627\u0641\u062a\u0647\u0627 \u0625\u0644\u0649 \u0633\u0644\u0629 \u0627\u0644\u062a\u0633\u0648\u0642 \u0627\u0644\u0645\u0648\u062c\u0648\u062f\u0629 \u062d\u0627\u0644\u064a\u0627\u064b.",
    "widget\u0004currently available: %s": "\u0645\u062a\u0648\u0641\u0631 \u062d\u0627\u0644\u064a\u0627: %s",
    "widget\u0004from %(currency)s %(price)s": "\u0645\u0646 %(currency) s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "\u064a\u0634\u0645\u0644 %(rate)s% %(taxname)s",
    "widget\u0004incl. taxes": "\u0634\u0627\u0645\u0644 \u0627\u0644\u0636\u0631\u064a\u0628\u0629",
    "widget\u0004minimum amount to order: %s": "\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 \u0644\u0644\u0637\u0644\u0628: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "\u0628\u0627\u0644\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 %(rate)s% %(taxname)s",
    "widget\u0004plus taxes": "\u0628\u0627\u0644\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 \u0627\u0644\u0636\u0631\u0627\u0626\u0628"
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P",
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%m/%d/%Y %H:%M:%S",
      "%m/%d/%Y %H:%M:%S.%f",
      "%m/%d/%Y %H:%M",
      "%m/%d/%y %H:%M:%S",
      "%m/%d/%y %H:%M:%S.%f",
      "%m/%d/%y %H:%M"
    ],
    "DATE_FORMAT": "j F\u060c Y",
    "DATE_INPUT_FORMATS": [
      "%d-%m-%Y",
      "%Y-%m-%d",
      "%m/%d/%Y",
      "%m/%d/%y",
      "%b %d %Y",
      "%b %d, %Y",
      "%d %b %Y",
      "%d %b, %Y",
      "%B %d %Y",
      "%B %d, %Y",
      "%d %B %Y",
      "%d %B, %Y"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 0,
    "MONTH_DAY_FORMAT": "j F",
    "NUMBER_GROUPING": 0,
    "SHORT_DATETIME_FORMAT": "m/d/Y P",
    "SHORT_DATE_FORMAT": "d\u200f/m\u200f/Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "g:i A",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};

