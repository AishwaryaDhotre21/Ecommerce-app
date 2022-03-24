from django.shortcuts import redirect


def auth_middleware1(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if not request.session.get('cart'):
            return redirect('homepage')
        #else:
            #return redirect('cartpage')
        print('middleware')
        response = get_response(request)
        return response

    return middleware