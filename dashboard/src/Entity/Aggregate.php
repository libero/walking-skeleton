<?php

namespace Libero\Dashboard\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Embeddable
 */
final class Aggregate
{
    /**
     * @ORM\Column(type="string")
     */
    private $service;

    /**
     * @ORM\Column(type="string")
     */
    private $name;

    /**
     * @ORM\Column(type="string")
     */
    private $identifier;

    public function __construct(string $service, string $name, string $identifier)
    {
        $this->service = $service;
        $this->name = $name;
        $this->identifier = $identifier;
    }

    public function getIdentifier() : string
    {
        return $this->identifier;
    }

    public function getName() : string
    {
        return $this->name;
    }

    public function getService() : string
    {
        return $this->service;
    }
}
