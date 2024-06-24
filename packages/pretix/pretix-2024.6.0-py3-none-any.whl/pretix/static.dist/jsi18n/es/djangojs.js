

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = n != 1;
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
      "(una fecha m\u00e1s)",
      "({num} m\u00e1s fechas)"
    ],
    "Add condition": "A\u00f1adir condici\u00f3n",
    "Additional information required": "Se requiere informaci\u00f3n adicional",
    "All": "Todos",
    "All of the conditions below (AND)": "Todas las siguientes condiciones (Y)",
    "An error has occurred.": "Ha ocurrido un error.",
    "An error of type {code} occurred.": "Ha ocurrido un error de tipo {code}.",
    "April": "Abril",
    "At least one of the conditions below (OR)": "Al menos una de las siguientes condiciones (O)",
    "August": "Agosto",
    "Barcode area": "\u00c1rea para c\u00f3digo de barras",
    "Calculating default price\u2026": "Calculando el precio por defecto\u2026",
    "Cancel": "Cancelar",
    "Canceled": "Cancelado",
    "Cart expired": "El carrito de compras ha expirado",
    "Check-in QR": "QR de Chequeo",
    "Checked-in Tickets": "Registro de c\u00f3digo QR",
    "Click to close": "Click para cerrar",
    "Close message": "Cerrar mensaje",
    "Comment:": "Comentario:",
    "Confirming your payment \u2026": "Confirmando el pago\u2026",
    "Contacting Stripe \u2026": "Contactando con Stripe\u2026",
    "Contacting your bank \u2026": "Contactando con el banco\u2026",
    "Continue": "Continuar",
    "Copied!": "\u00a1Copiado!",
    "Count": "Cantidad",
    "Credit Card": "Tarjeta de cr\u00e9dito",
    "Current date and time": "Fecha y hora actual",
    "Currently inside": "Actualmente adentro",
    "December": "Diciembre",
    "Do you really want to leave the editor without saving your changes?": "\u00bfRealmente desea salir del editor sin haber guardado sus cambios?",
    "Entry": "Ingreso",
    "Entry not allowed": "Entrada no permitida",
    "Error while uploading your PDF file, please try again.": "Ha habido un error mientras se cargaba el archivo PDF, por favor, intente de nuevo.",
    "Event admission": "Admisi\u00f3n al evento",
    "Event end": "Fin del evento",
    "Event start": "Inicio del evento",
    "Exit": "Salida",
    "Exit recorded": "Salida registrada",
    "February": "Febrero",
    "Fr": "Vie",
    "Gate": "Puerta",
    "Generating messages \u2026": "Generando mensajes\u2026",
    "Group of objects": "Grupo de objetos",
    "Image area": "\u00c1rea de imagen",
    "Information required": "Informaci\u00f3n requerida",
    "January": "Enero",
    "July": "Julio",
    "June": "Junio",
    "Load more": "Cargar m\u00e1s",
    "March": "Marzo",
    "Marked as paid": "Marcado como pagado",
    "May": "Mayo",
    "Mo": "Lun",
    "No": "No",
    "No active check-in lists found.": "No se encontraron listas de registro activas.",
    "No tickets found": "No se encontraron tickets",
    "None": "Ninguno",
    "November": "Noviembre",
    "Number of days with a previous entry": "N\u00famero de d\u00edas con una entrada previa",
    "Number of previous entries": "N\u00famero de entradas previas",
    "Number of previous entries since midnight": "N\u00famero de entradas previas desde medianoche",
    "Object": "Objeto",
    "October": "Octubre",
    "Order canceled": "Orden cancelada",
    "Others": "Otros",
    "Paid orders": "\u00d3rdenes pagadas",
    "Placed orders": "\u00d3rdenes enviadas",
    "Please enter a quantity for one of the ticket types.": "Por favor, introduzca un valor para cada tipo de entrada.",
    "Please enter the amount the organizer can keep.": "Por favor, ingrese el monto que el organizador puede quedarse.",
    "Powered by pretix": "Prove\u00eddo por pretix",
    "Press Ctrl-C to copy!": "\u00a1Presione Control+C para copiar!",
    "Product": "Producto",
    "Product variation": "Ver variaciones del producto",
    "Redeemed": "Canjeado",
    "Result": "Resultado",
    "Sa": "S\u00e1b",
    "Saving failed.": "El guardado fall\u00f3.",
    "Scan a ticket or search and press return\u2026": "Escanee un ticket o busque y presione regresar\u2026",
    "Search query": "Consultar b\u00fasqueda",
    "Search results": "Resultados de b\u00fasqueda",
    "Select a check-in list": "Seleccione una lista de registro",
    "Selected only": "Solamente seleccionados",
    "September": "Septiembre",
    "Su": "Dom",
    "Switch check-in list": "Cambiar lista de registro",
    "Switch direction": "Cambiar direcci\u00f3n",
    "Text object": "Objeto de texto",
    "Th": "Jue",
    "The PDF background file could not be loaded for the following reason:": "El archivo PDF de fondo no ha podido ser cargado debido al siguiente motivo:",
    "The items in your cart are no longer reserved for you. You can still complete your order as long as they\u2019re available.": "Los elementos en su carrito de compras ya no se encuentran reservados. Puedes seguir a\u00f1adiendo m\u00e1s productos mientras est\u00e9n disponibles.",
    "The items in your cart are reserved for you for one\u00a0minute.": [
      "Los elementos en su carrito de compras se han reservado por {num} minutos.",
      "Los elementos en su carrito de compras se han reservado por {num} minutos."
    ],
    "The organizer keeps %(currency)s %(amount)s": "El organizador se queda %(currency)s %(price)s",
    "The request took too long. Please try again.": "La solicitud ha tomado demasiado tiempo. Por favor, intente de nuevo.",
    "This ticket is not yet paid. Do you want to continue anyways?": "Este ticket a\u00fan no ha sido pagado \u00bfDesea continuar de todos modos?",
    "This ticket requires special attention": "Este ticket requiere atenci\u00f3n especial",
    "Ticket already used": "Este ticket ya fue utilizado",
    "Ticket blocked": "Ticket bloqueado",
    "Ticket code revoked/changed": "C\u00f3digo de ticket revocado/cambiado",
    "Ticket design": "Dise\u00f1o del ticket",
    "Ticket not paid": "Ticket por pagar",
    "Ticket not valid at this time": "Ticket no v\u00e1lido en este momento",
    "Ticket type not allowed here": "Tipo de ticket no est\u00e1 permitido",
    "Time zone:": "Zona horaria:",
    "Tolerance (minutes)": "Tolerancia (en minutos)",
    "Total": "Total",
    "Total revenue": "Ingresos totales",
    "Tu": "Mar",
    "Unknown error.": "Error desconocido.",
    "Unknown ticket": "Ticket no encontrado",
    "Unpaid": "Por pagar",
    "Use a different name internally": "Usar un nombre diferente internamente",
    "Valid": "V\u00e1lido",
    "Valid Tickets": "Tickets v\u00e1lidos",
    "Valid ticket": "Ticket v\u00e1lido",
    "We": "Mi\u00e9",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "Estamos enviando su solicitud al servidor. Si este proceso toma m\u00e1s de un minuto, por favor, revise su conexi\u00f3n a Internet, recargue la p\u00e1gina e intente nuevamente.",
    "We are processing your request \u2026": "Estamos procesando su solicitud\u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "Ahora mismo no podemos contactar con el servidor, pero lo seguimos intentando. El \u00faltimo c\u00f3digo de error fue: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "Ahora mismo no podemos contactar con el servidor. Por favor, intente de nuevo. C\u00f3digo de error: {code}",
    "Yes": "S\u00ed",
    "You get %(currency)s %(amount)s back": "Obtienes %(currency)s %(price)s de vuelta",
    "You have unsaved changes!": "\u00a1Tienes cambios sin guardar!",
    "Your color has bad contrast for text on white background, please choose a darker shade.": "Tu color tiene mal contraste para un texto con fondo blanco, por favor, escoge un tono m\u00e1s oscuro.",
    "Your color has decent contrast and is probably good-enough to read!": "\u00a1Tu color tiene un contraste decente y es probablemente lo suficientemente legible!",
    "Your color has great contrast and is very easy to read!": "\u00a1Tu color tiene gran contraste y es muy f\u00e1cil de leer!",
    "Your local time:": "Su hora local:",
    "Your request arrived on the server but we still wait for it to be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "Su solicitud lleg\u00f3 al servidor pero seguimos esperando a que sea procesada. Si toma m\u00e1s de dos minutos, por favor cont\u00e1ctenos o regrese a la p\u00e1gina anterior en su navegador e intente de nuevo.",
    "Your request has been queued on the server and will soon be processed.": "Su solicitud ha sido enviada al servidor y ser\u00e1 procesada en breve.",
    "Your request is currently being processed. Depending on the size of your event, this might take up to a few minutes.": "Su solicitud est\u00e1 siendo procesada. Esto puede tardar varios minutos, dependiendo del tama\u00f1o de su evento.",
    "close": "Cerrar",
    "custom date and time": "seleccionar fecha y hora",
    "custom time": "seleccionar hora",
    "is after": "est\u00e1 despu\u00e9s",
    "is before": "est\u00e1 antes",
    "is one of": "es uno de",
    "minutes": "minutos",
    "required": "campo requerido",
    "widget\u0004Back": "Atr\u00e1s",
    "widget\u0004Buy": "Comprar",
    "widget\u0004Choose a different date": "Elegir una fecha diferente",
    "widget\u0004Choose a different event": "Eligir un evento diferente",
    "widget\u0004Close": "Cerrar",
    "widget\u0004Close ticket shop": "Cerrar tienda de tickets",
    "widget\u0004Continue": "Continuar",
    "widget\u0004FREE": "GRATIS",
    "widget\u0004Load more": "Cargar m\u00e1s",
    "widget\u0004Next month": "Siguiente mes",
    "widget\u0004Next week": "Semana siguiente",
    "widget\u0004Only available with a voucher": "Solo disponible mediante voucher",
    "widget\u0004Open seat selection": "Abrir selecci\u00f3n de asientos",
    "widget\u0004Open ticket shop": "Abrir tienda de tickets",
    "widget\u0004Previous month": "Mes anterior",
    "widget\u0004Previous week": "Semana anterior",
    "widget\u0004Redeem": "Canjear",
    "widget\u0004Redeem a voucher": "Canjear un cup\u00f3n",
    "widget\u0004Register": "Registrarse",
    "widget\u0004Reserved": "Reservado",
    "widget\u0004Resume checkout": "Continuar pago",
    "widget\u0004Sold out": "Agotado",
    "widget\u0004The cart could not be created. Please try again later": "El carrito de compras no ha podido crearse. Por favor, intente de nuevo m\u00e1s tarde",
    "widget\u0004The ticket shop could not be loaded.": "No se ha podido cargar la tienda de tickets.",
    "widget\u0004There are currently a lot of users in this ticket shop. Please open the shop in a new tab to continue.": "Actualmente hay muchos usuarios en la tienda de tickets. Por favor abra la tienda en una nueva pesta\u00f1a para continuar.",
    "widget\u0004Voucher code": "C\u00f3digo del cup\u00f3n",
    "widget\u0004Waiting list": "Lista de espera",
    "widget\u0004We could not create your cart, since there are currently too many users in this ticket shop. Please click \"Continue\" to retry in a new tab.": "No pudimos crear su carrito debido a que hay muchos usuarios en la tienda. Por favor, presione \"Continuar\" para intentarlo en una nueva pesta\u00f1a.",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "Ya tiene un carrito de compras activo para este evento. Si selecciona m\u00e1s productos, estos ser\u00e1n a\u00f1adidos al carrito actual.",
    "widget\u0004currently available: %s": "disponible actualmente: %s",
    "widget\u0004from %(currency)s %(price)s": "desde %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "incluye %(rate)s% %(taxname)s",
    "widget\u0004incl. taxes": "incl. impuestos",
    "widget\u0004minimum amount to order: %s": "cantidad m\u00ednima a ordenar: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "m\u00e1s %(rate)s% %(taxname)s",
    "widget\u0004plus taxes": "m\u00e1s impuestos"
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
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
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

