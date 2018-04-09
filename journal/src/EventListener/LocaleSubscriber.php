<?php

namespace Libero\Journal\EventListener;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\GetResponseEvent;
use Symfony\Component\HttpKernel\KernelEvents;
use Symfony\Component\Translation\TranslatorInterface;

final class LocaleSubscriber implements EventSubscriberInterface
{
    private const ATTRIBUTE = 'locale';

    private $translator;

    public static function getSubscribedEvents() : array
    {
        return [
            KernelEvents::REQUEST => [['onKernelRequest', 20]],
        ];
    }

    public function __construct(TranslatorInterface $translator)
    {
        $this->translator = $translator;
    }

    public function onKernelRequest(GetResponseEvent $event) : void
    {
        if (!$event->isMasterRequest()) {
            return;
        }

        $request = $event->getRequest();

        if ($locale = $request->query->get(self::ATTRIBUTE)) {
            if (in_array($locale, $this->translator->getFallbackLocales())) {
                $request->getSession()->set('_locale', $locale);
            }
        }

        if ($locale = $request->getSession()->get('_locale')) {
            $request->setLocale($locale);
        }
    }
}
