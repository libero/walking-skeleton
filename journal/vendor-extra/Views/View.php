<?php

namespace Libero\Views;

use function array_merge_recursive;

final class View
{
    private $arguments;
    private $template;

    public function __construct(string $template, array $arguments = [])
    {
        $this->template = $template;
        $this->arguments = $arguments;
    }

    public function getArguments() : array
    {
        return $this->arguments;
    }

    public function getTemplate() : string
    {
        return $this->template;
    }

    public function withArguments(array $arguments) : View
    {
        if ($arguments === $this->arguments) {
            return $this;
        }

        $view = clone $this;

        $view->arguments = array_merge_recursive($view->arguments, $arguments);

        return $view;
    }

    public function withTemplate(string $template) : View
    {
        if ($template === $this->template) {
            return $this;
        }

        $view = clone $this;

        $view->template = $template;

        return $view;
    }
}