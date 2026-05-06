using BackendSpa.Application.Common.Responsive;
using BackendSpa.Application.Interfaces;
using Twilio;
using Twilio.Rest.Api.V2010.Account;

namespace BackendSpa.Infrastructure.Services
{
    public class TwilioService : INotificacion
    {
        private readonly string _fromNumber;

        public TwilioService(IConfiguration config)
        {
            var accountSid = config["Twilio:AccountSid"]!;
            var authToken = config["Twilio:AuthToken"]!;
            _fromNumber = config["Twilio:PhoneNumber"]!;

            TwilioClient.Init(accountSid, authToken);
        }

        public async Task<Responsive<bool>> EnviarMensajeAsync(string destinatario, string mensaje)
        {
            try
            {
                var message = await MessageResource.CreateAsync(
                    to: new Twilio.Types.PhoneNumber(destinatario),
                    from: new Twilio.Types.PhoneNumber(_fromNumber),
                    body: mensaje
                );

                return new Responsive<bool>(true, "", true);
            }
            catch (Exception ex)
            {
                return new Responsive<bool>(false, $"Error Twilio: {ex.Message}", false);
            }
        }
    }
}
