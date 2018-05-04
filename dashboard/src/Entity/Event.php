<?php

namespace Libero\Dashboard\Entity;

use DateTimeImmutable;
use DateTimeZone;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table
 */
final class Event
{
    /**
     * @ORM\Column(type="datetime_immutable")
     */
    private $dateTime;

    /**
     * @ORM\Column(type="guid")
     * @ORM\Id
     */
    private $id;

    /**
     * @ORM\Column(type="string")
     */
    private $type;

    public function __construct(string $id, DateTimeImmutable $dateTime, string $type)
    {
        $this->id = $id;
        $this->dateTime = $dateTime->setTimezone(new DateTimeZone('UTC'));
        $this->type = $type;
    }

    public function getId() : string
    {
        return $this->id;
    }

    public function getDateTime() : DateTimeImmutable
    {
        return $this->dateTime;
    }

    public function getType() : string
    {
        return $this->type;
    }
}
